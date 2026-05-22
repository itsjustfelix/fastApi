from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime,timedelta, timezone
import os
from dotenv import load_dotenv

from utils.error_structure import error_response

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFERSH")
security = HTTPBearer()

def crear_token_acceso(codigo_usuario: str, codigo_rol: str) -> str:
    payload = {
        "sub": codigo_usuario,
        "rol": codigo_rol,
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=15)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def crear_token_refresco(codigo_usuario: str) -> str:
    payload = {
        "sub": codigo_usuario,
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY_REFRESH, algorithm=ALGORITHM)


def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail=error_response("TOKEN_EXPIRED", "El token ha expirado")
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail=error_response("TOKEN_INVALID", "El token ha sido modificado o es inválido")
        )
    

def verificar_token_refresh(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY_REFRESH, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail=error_response("TOKEN_EXPIRED", "El token de refresco ha expirado")
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail=error_response("TOKEN_INVALID", "El token de refresco ha sido modificado o es inválido")
        )