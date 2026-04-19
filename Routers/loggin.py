from fastapi import APIRouter
import oracledb
from utils.passwordHasser import verificar_password
from database.conexion import get_connection

router = APIRouter(
    prefix="/login",
    tags=["login"]
)

@router.post("")
def login(email: str, password: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        codigo_usuario_out = cursor.var(oracledb.STRING)
        contraseña_out = cursor.var(oracledb.STRING)
        codigo_rol_out = cursor.var(oracledb.STRING)
        cursor.callproc("PKG_USUARIO.PRC_buscar_usuario_por_email", [email, codigo_usuario_out, contraseña_out, codigo_rol_out])

        verificaion_result = verificar_password(password, contraseña_out.getvalue())
        if verificaion_result:
            return {"message": "Login exitoso", "codigo_usuario": codigo_usuario_out.getvalue(), "codigo_rol": codigo_rol_out.getvalue()}
        else:
            return {"message": "Credenciales inválidas"}

    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()