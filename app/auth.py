from bcrypt import checkpw, hashpw, gensalt


def hash_password(password: str) -> str:
    password = password.encode()
    password_hashed = hashpw(password, gensalt())
    return password_hashed.decode()

def check_password(password: str, password_hashed: str) -> bool:
    password = password.encode()
    password_hashed = password_hashed.encode()
    return checkpw(password, password_hashed)
