# small helper module - kept simple as a student would
def pretty_count(n):
    if n < 1000:
        return str(n)
    return f"{n:,}"  # group thousands, maybe overkill but handy
