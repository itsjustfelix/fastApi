from jose import jwt
from datetime import datetime,timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def crear_token(codigo_usuario: str, codigo_rol: str) -> str:
    payload = {
        "sub": codigo_usuario,
        "rol": codigo_rol,
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)