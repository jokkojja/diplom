from werkzeug.security import generate_password_hash, check_password_hash


def password_encoding(password: str, method: str) -> str:
    hashed_password = generate_password_hash(password, method=method)[len(method):]
    return hashed_password


def check_password(password: str, encoded_password: str, method: str) -> bool:
    return check_password_hash(method + encoded_password, password)