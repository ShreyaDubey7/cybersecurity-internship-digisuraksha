import re
import bcrypt
from typing import Tuple

COMMON_PASSWORDS = {
    "password","123456","12345678","qwerty","abc123","111111","password1"
}

SYMBOLS_RE = re.compile(r"[!@#$%^&*(),.?\":{}|<>\\\[\\];'`~_+=/-]")


def hash_password(plain: str) -> bytes:
    """Hash password with bcrypt and return bytes."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain.encode('utf-8'), salt)


def check_password(plain: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(plain.encode('utf-8'), hashed)


def password_strength(password: str) -> Tuple[int, dict]:
    """Return strength score (0-100) and details dictionary.

    Simple heuristic:
    - length
    - upper/lower
    - digits
    - symbols
    - not common
    """
    score = 0
    details = {
        'length': False,
        'upper': False,
        'lower': False,
        'digit': False,
        'symbol': False,
        'not_common': True,
    }

    if len(password) >= 8:
        score += 30
        details['length'] = True
    elif len(password) >= 6:
        score += 10

    if re.search(r'[A-Z]', password):
        score += 15
        details['upper'] = True
    if re.search(r'[a-z]', password):
        score += 15
        details['lower'] = True
    if re.search(r'\d', password):
        score += 15
        details['digit'] = True
    if SYMBOLS_RE.search(password):
        score += 15
        details['symbol'] = True

    if password.lower() in COMMON_PASSWORDS or len(password) < 4:
        details['not_common'] = False
        score = max(score - 30, 0)

    # clamp
    score = max(0, min(100, score))
    return score, details

