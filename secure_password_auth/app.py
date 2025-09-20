from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import sqlite3
from pathlib import Path
from utils.password_utils import hash_password, check_password, password_strength
import time

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / 'db' / 'users.db'

app = Flask(__name__)
app.secret_key = 'replace-with-a-secure-random-key'  # replace in production

# Simple in-memory brute-force protection (per IP). For production use Redis/more robust store.
FAILED_ATTEMPTS = {}
BLOCK_TIME_SECONDS = 300
MAX_FAILED = 5


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.before_request
def before_request():
    g.db = get_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def log_event(username, event):
    ip = request.remote_addr
    cur = g.db.cursor()
    cur.execute('INSERT INTO audit_logs (username, event, ip) VALUES (?, ?, ?)', (username, event, ip))
    g.db.commit()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        score, details = password_strength(password)
        if score < 50:
            flash('Password too weak. Please choose a stronger password.')
            return redirect(url_for('register'))

        pw_hash = hash_password(password)
        cur = g.db.cursor()
        try:
            cur.execute('INSERT INTO users (username, password_hash) VALUES (?,?)', (username, pw_hash))
            g.db.commit()
            log_event(username, 'register')
            flash('Registration successful — please log in')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already taken')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    ip = request.remote_addr
    entry = FAILED_ATTEMPTS.get(ip, {'count': 0, 'first_failed': None, 'blocked_until': 0})

    now = time.time()
    if entry.get('blocked_until', 0) > now:
        flash('Too many failed attempts. Try again later.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        cur = g.db.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cur.fetchone()
        if row and check_password(password, row['password_hash']):
            session.clear()
            session['user'] = username
            # reset attempts
            FAILED_ATTEMPTS.pop(ip, None)
            log_event(username, 'login_success')
            return redirect(url_for('index'))
        else:
            # register failed attempt
            entry = FAILED_ATTEMPTS.setdefault(ip, {'count': 0, 'first_failed': now, 'blocked_until': 0})
            entry['count'] += 1
            if entry['count'] >= MAX_FAILED:
                entry['blocked_until'] = now + BLOCK_TIME_SECONDS
            FAILED_ATTEMPTS[ip] = entry
            log_event(username, 'login_failed')
            flash('Invalid credentials')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    user = session.pop('user', None)
    if user:
        log_event(user, 'logout')
    flash('Logged out')
    return redirect(url_for('index'))


if __name__ == '__main__':
    if not DB_PATH.exists():
        import init_db
    app.run(debug=True)
