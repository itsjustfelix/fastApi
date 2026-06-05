from fastapi import APIRouter, HTTPException, Depends
from models.administradores import Administradores_create, Administradores_show, Administradores_update
from database.conexion import get_connection
from utils.passwordHasser import hashear_password
from utils.token import verificar_token
from utils.error_structure import error_response

import oracledb
router = APIRouter(
    prefix="/administradores",
    tags=["administradores"]
)

@router.get("")
def get_administradores(token: dict = Depends(verificar_token)):
    
    if token["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para ver administradores")
        )
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        datos_cursor = cursor.callfunc("PKG_ADMINISTRADORES.FN_CONSULTAR", oracledb.CURSOR, [])

        if datos_cursor:
            columnas = [col[0].lower() for col in datos_cursor.description]
            administradores = []
            for fila in datos_cursor:
                administradores.append(Administradores_show(**dict(zip(columnas, fila))))
            return administradores
        else:
            return []

    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(
                status_code=401,
                detail=error_response("UNAUTHORIZED", "Credenciales incorrectas")
            )
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("", status_code=201)
def create_administrador(admin: Administradores_create, token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(
            status_code=403, 
            detail=error_response("FORBIDDEN", "Rol no autorizado para crear administradores"))
    try:
        conn = get_connection()
        cursor = conn.cursor()

        codigo_usuario = cursor.callfunc("PKG_USUARIO.FN_guardar_usuario",
                                        str,
                                        [admin.email, 
                                         hashear_password(admin.contraseña), 
                                         admin.rol])

        cursor.callproc("PKG_ADMINISTRADORES.PRC_GUARDAR",
                        [admin.cedula,
                         admin.nombreCompleto,
                         admin.telefono,
                         codigo_usuario])
        conn.commit()
        return {"message": "Administrador creado correctamente."}

    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args

        if "ORA-00001" in str(error.message):
            raise HTTPException(
                status_code=409,
                detail=error_response("CONFLICT", "La cédula o correo ya está registrado")
            )
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=error_response("SERVER_ERROR", "Error interno del servidor", [{"message": str(e)}])
        )
    finally:
        cursor.close()
        conn.close()

@router.put("/",status_code=200)
def update_administrador(admin: Administradores_update, token: dict = Depends(verificar_token)):
    if token["rol"] != "1":
        raise HTTPException(
            status_code=403, 
            detail=error_response("FORBIDDEN", "No autorizado para actualizar administradores"))
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_ADMINISTRADORES.PRC_ACTUALIZAR",
                        [admin.cedula,
                         admin.nombreCompleto,
                         admin.telefono])
        conn.commit()
        
        return {"message": "Administrador actualizado correctamente."}
    except HTTPException:
       raise
    
    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=error_response("SERVER_ERROR", "Error interno del servidor", [{"message": str(e)}])
        )
    finally:
        cursor.close()
        conn.close()

@router.delete("/{administrador_id}", status_code=200)
def delete_administrador(administrador_id: str, token: dict = Depends(verificar_token)):
    
    if token["rol"] != "1":
        raise HTTPException(
            status_code=403, 
            detail=error_response("FORBIDDEN", "No autorizado para eliminar administradores"))
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_ADMINISTRADORES.PRC_ELIMINAR", [administrador_id])
        conn.commit()
        return {"message": "Administrador eliminado correctamente."}
    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=error_response("SERVER_ERROR", "Error interno del servidor", [{"message": str(e)}])
        )
    finally:
        cursor.close()
        conn.close()