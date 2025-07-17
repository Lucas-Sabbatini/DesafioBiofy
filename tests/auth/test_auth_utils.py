from app.auth.utils import get_password_hash, verify_password

def test_get_password_hash():
    """
    Testa se a função get_password_hash retorna um hash.
    O hash não deve ser igual à senha original.
    """
    password = "plain_password"
    hashed_password = get_password_hash(password)
    assert hashed_password is not None
    assert isinstance(hashed_password, str)
    assert password != hashed_password

def test_verify_password_correct():
    """
    Testa se verify_password retorna True para a senha correta.
    """
    password = "correct_password"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) is True

def test_verify_password_incorrect():
    """
    Testa se verify_password retorna False para uma senha incorreta.
    """
    password = "correct_password"
    wrong_password = "wrong_password"
    hashed_password = get_password_hash(password)
    assert verify_password(wrong_password, hashed_password) is False
