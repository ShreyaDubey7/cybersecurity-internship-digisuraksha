from flask import Flask, request, redirect, render_template_string
import sqlite3
import string
import random
import os

app = Flask(__name__)

DB_FILE = 'urls.db'

# HTML Template
TEMPLATE = """
<!doctype html>
<title>URL Shortener</title>
<h1>Shorten Your URL</h1>
<form method=post>
  <input type=text name=long_url placeholder="Enter long URL" required>
  <input type=submit value=Shorten>
</form>
{% if short_url %}
  <p>Short URL: <a href="{{ short_url }}">{{ short_url }}</a></p>
{% endif %}
"""

# DB Initialization
def init_db():
    if not os.path.exists(DB_FILE):
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute('CREATE TABLE urls (id INTEGER PRIMARY KEY AUTOINCREMENT, long_url TEXT, short_code TEXT UNIQUE)')
            conn.commit()

# Generate random short code
def generate_short_code(length=6):
    homoglyphs = [
        'a', 'а',  # Latin and Cyrillic 'a'
        'b', 'Ь',  # Latin 'b', Cyrillic soft sign
        'c', 'с',  # Latin and Cyrillic 'c'
        'e', 'е',  # Latin and Cyrillic 'e'
        'i', 'і', '1', 'l', 'I',  # visually similar 'i'
        'l', '1', 'I',  # visually similar 'l'
        'o', '0', 'О',  # Latin 'o', digit zero, Cyrillic O
        'p', 'ρ',  # Latin 'p', Greek rho
        's', 'ѕ',  # Latin 's', Cyrillic s
        'x', 'х',  # Latin 'x', Cyrillic x
        'y', 'у',  # Latin 'y', Cyrillic u
        'z', 'ᴢ'   # Latin z, small cap Z
    ]

    return ''.join(random.choices(homoglyphs, k=length))

# Store and retrieve from DB
def store_url(long_url):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        # Check if URL already exists
        cur.execute("SELECT short_code FROM urls WHERE long_url = ?", (long_url,))
        row = cur.fetchone()
        if row:
            return row[0]

        # Generate new unique short code
        while True:
            short_code = generate_short_code()
            cur.execute("SELECT 1 FROM urls WHERE short_code = ?", (short_code,))
            if not cur.fetchone():
                break

        cur.execute("INSERT INTO urls (long_url, short_code) VALUES (?, ?)", (long_url, short_code))
        conn.commit()
        return short_code

def get_long_url(short_code):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT long_url FROM urls WHERE short_code = ?", (short_code,))
        row = cur.fetchone()
        return row[0] if row else None

# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_code = store_url(long_url)
        spoofed_prefix = "https://ɡooɡle.com/"  # both 'ɡ' are Unicode Latin small letter script G (U+0261)
        short_url = spoofed_prefix + short_code

    return render_template_string(TEMPLATE, short_url=short_url)

@app.route('/<short_code>')
def redirect_to_url(short_code):
    long_url = get_long_url(short_code)
    if long_url:
        return redirect(long_url)
    return "Invalid short URL", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
