from fastapi import APIRouter, HTTPException
import oracledb
from utils.passwordHasser import verificar_password
from database.conexion import get_connection
from models.login import Login
from jose import jwt
from datetime import datetime,timedelta, timezone
import os
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(
    prefix="/login",
    tags=["login"]
)


def crear_token(codigo_usuario: str, codigo_rol: str) -> str:
    payload = {
        "sub": codigo_usuario,
        "rol": codigo_rol,
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.post("")
def login(datos : Login):
    try:
        conn = get_connection()
        cursor = conn.cursor()
    
        codigo_usuario_out = cursor.var(oracledb.STRING)
        contraseña_out = cursor.var(oracledb.STRING)
        codigo_rol_out = cursor.var(oracledb.STRING)

        cursor.callproc("PKG_USUARIO.PRC_buscar_usuario_por_email", 
                        [datos.email,
                          codigo_usuario_out, 
                          contraseña_out, 
                          codigo_rol_out])
        
        if not verificar_password(datos.contraseña, contraseña_out.getvalue()):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
        token = crear_token(
            codigo_usuario_out.getvalue(),
            codigo_rol_out.getvalue()
        )
        return{
            "token": token,
            "rol": codigo_rol_out.getvalue()
        }
        
    except HTTPException:
       raise

    except oracledb.DatabaseError as e:
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        raise HTTPException(status_code=500, detail="Error en la base de datos")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()