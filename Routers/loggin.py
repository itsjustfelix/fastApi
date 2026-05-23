from fastapi import APIRouter, HTTPException, Response, Request
import oracledb
from utils.error_structure import error_response
from utils.passwordHasser import verificar_password
from database.conexion import get_connection
from models.login import Login
from utils.token import crear_token_acceso, crear_token_refresco, verificar_token_refresh

router = APIRouter(
    prefix="/login",
    tags=["login"]
)

@router.post("", status_code=200)
def login(datos : Login, response: Response):
    try:
        conn = get_connection()
        cursor = conn.cursor()
    
        codigo_usuario_out = cursor.var(oracledb.STRING)
        contraseña_out     = cursor.var(oracledb.STRING)
        codigo_rol_out     = cursor.var(oracledb.STRING)

        cursor.callproc(
            "PKG_USUARIO.PRC_buscar_usuario_por_email", 
                        [datos.email,
                          codigo_usuario_out, 
                          contraseña_out, 
                          codigo_rol_out])
        
        if not verificar_password(datos.contraseña, contraseña_out.getvalue()):
            raise HTTPException(status_code=401, detail=error_response("UNAUTHORIZED", "Credenciales incorrectas"))
        
        nombre = buscar_nombre_por_codigo_usuario(
            codigo_rol=codigo_rol_out.getvalue(),
            codigo_usuario= codigo_usuario_out.getvalue()
        )

        token_acceso = crear_token_acceso(
            codigo_usuario_out.getvalue(),
            codigo_rol_out.getvalue()
        )

        token_refresco = crear_token_refresco(
            codigo_usuario_out.getvalue()
        )

        response.set_cookie(
            key="token_refresco",
            value=token_refresco,
            httponly=True,
            samesite="lax",
            max_age=7*24*60*60
        ) 

        cursor.callproc("PKG_USUARIO.prc_registrar_token_refresh", 
                        [codigo_usuario_out.getvalue(), token_refresco])
        
        conn.commit()

        return{
            "token" : token_acceso,
            "rol"   : codigo_rol_out.getvalue(),
            "nombre": nombre,
            "codigo_usuario": codigo_usuario_out.getvalue()
        }
        
    except HTTPException:
       raise

    except oracledb.DatabaseError as e:
        error, = e.args
        conn.rollback()  
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail=error_response("UNAUTHORIZED", "Credenciales incorrectas"))
        raise HTTPException(status_code=500, detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}]))

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", str(e)))
    finally:
        cursor.close()
        conn.close()

@router.post("/refresh", status_code=200)
def refresh_token(request: Request):
    try:
        
        refresh_token_cookie = request.cookies.get("token_refresco")
        print("Token de refresco recibido:", refresh_token_cookie)  # Debug: Verificar que el token se recibe correctamente

        if not refresh_token_cookie:
            raise HTTPException(
                status_code=401,
                detail=error_response("UNAUTHORIZED", "No hay token de refresco")
            )

        payload = verificar_token_refresh(refresh_token_cookie)  # Esto lanzará una excepción si el token no es válido o ha expirado

        codigo_usuario = payload.get("sub")

        conn = get_connection()
        cursor = conn.cursor()

        refresh_db_out = cursor.var(oracledb.STRING)
        codigo_rol_out = cursor.var(oracledb.STRING)

        cursor.callproc("PKG_USUARIO.PRC_BUSCAR_REFRESH_TOKEN",
                        [codigo_usuario, refresh_db_out, codigo_rol_out])

        if refresh_db_out.getvalue() != refresh_token_cookie:
            raise HTTPException(
                status_code=403,
                detail=error_response("FORBIDDEN", "Token revocado o no coincide")
            )

        nuevo_access_token = crear_token_acceso(codigo_usuario, codigo_rol_out.getvalue())

        return {"token": nuevo_access_token}

    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        error, = e.args
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("INTERNAL_SERVER_ERROR", str(e))
        )
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


@router.post("/logout", status_code=200)
def logout(request: Request, response: Response):
    try:
        refresh_token_cookie = request.cookies.get("token_refresco")

        if refresh_token_cookie:
            payload = verificar_token_refresh(refresh_token_cookie)
            codigo_usuario = payload.get("sub")

            conn = get_connection()
            cursor = conn.cursor()

            cursor.callproc("PKG_USUARIO.prc_eliminar_refresh_token", [codigo_usuario])
            conn.commit()

        response.delete_cookie(key="token_refresco")
        return {"message": "Logout exitoso"}
    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        error, = e.args
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("INTERNAL_SERVER_ERROR", str(e))
        )
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
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
        