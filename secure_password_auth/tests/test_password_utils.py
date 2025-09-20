from utils.password_utils import password_strength, hash_password, check_password


def test_strength():
    s, d = password_strength('Short1!')
    assert isinstance(s, int)


def test_hash_and_check():
    p = 'MyS3cr3t!'
    h = hash_password(p)
    assert check_password(p, h)
    assert not check_password('wrong', h)
