import bcrypt

def hashear_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hash.decode("utf-8")

def verificar_password(password: str, hash: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hash.encode("utf-8")
    )