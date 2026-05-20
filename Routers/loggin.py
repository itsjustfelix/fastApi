from fastapi import APIRouter, HTTPException
import oracledb
from utils.error_structure import error_response
from utils.passwordHasser import verificar_password
from database.conexion import get_connection
from models.login import Login
from utils.token import crear_token


router = APIRouter(
    prefix="/login",
    tags=["login"]
)


@router.post("", status_code=200)
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
            raise HTTPException(status_code=401, detail=error_response("UNAUTHORIZED", "Credenciales incorrectas"))
        
        nombre = buscar_nombre_por_codigo_usuario(codigo_rol=codigo_rol_out.getvalue(),
                                                  codigo_usuario= codigo_usuario_out.getvalue())

        token = crear_token(
            codigo_usuario_out.getvalue(),
            codigo_rol_out.getvalue()
        )

        return{
            "token" : token,
            "rol"   : codigo_rol_out.getvalue(),
            "nombre": nombre,
            "codigo_usuario": codigo_usuario_out.getvalue()
        }
        
    except HTTPException:
       raise

    except oracledb.DatabaseError as e:
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail=error_response("UNAUTHORIZED", "Credenciales incorrectas"))
        raise HTTPException(status_code=500, detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}]))

    except Exception as e:
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", str(e)))
    finally:
        cursor.close()
        conn.close()

def buscar_nombre_por_codigo_usuario(codigo_rol: str, codigo_usuario: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        nombre = None

        match codigo_rol:
            case "1":
                nombre = cursor.callfunc("PKG_ADMINISTRADORES.FN_CONSULTAR_NOMBRE",
                                            str,
                                            [codigo_usuario])
            case "2":
                nombre = cursor.callfunc("PKG_VETERINARIOS.FN_CONSULTAR_NOMBRE",
                                            str,
                                            [codigo_usuario])
            case "3":
                nombre = cursor.callfunc("PKG_PROPIETARIOS.FN_CONSULTAR_NOMBRE",
                                            str,
                                            [codigo_usuario])
        return nombre
    except HTTPException:
       raise
    except oracledb.DatabaseError as e:
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail=error_response("UNAUTHORIZED", "Credenciales incorrectas"))
        raise HTTPException(status_code=500, detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}]))
    except Exception as e:
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", str(e)))
        