from fastapi import APIRouter, HTTPException, Depends
import oracledb
from models.propietarios import Propietarios_create, Propietarios_show, Propietarios_update
from database.conexion import get_connection
from utils.passwordHasser import hashear_password
from utils.token import verificar_token
from utils.error_structure import error_response

router = APIRouter(
    prefix="/propietarios",
    tags=["propietarios"]
)

@router.get("")
def get_propietarios(token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para ver propietarios")
        )
    try:
        conn = get_connection()
        cursor = conn.cursor()
        datos_cursor = cursor.callfunc(
            "PKG_PROPIETARIOS.FN_CONSULTAR",
            oracledb.CURSOR, []
        )
        
        columnas = [col[0].lower() for col in datos_cursor.description]
        propietarios = []
        for fila in datos_cursor:
            propietarios.append(Propietarios_show.model_validate(dict(zip(columnas, fila))))
        return propietarios

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
            detail=error_response("SERVER_ERROR", "Error interno del servidor", [{"message": str(e)}])
        )
    finally:
        cursor.close()
        conn.close()


@router.get("/{cedula_propietario}")
def get_propietario(cedula_propietario: str, token: dict = Depends(verificar_token)):
    if token["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para ver propietarios")
        )
        
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        
        nombre_var = cursor.var(oracledb.STRING)
        codigo_usuario_var = cursor.var(oracledb.STRING)
        
        
        cursor.callproc(
            "PKG_PROPIETARIOS.PRC_CONSULTAR_POR_CEDULA",
            [cedula_propietario, nombre_var, codigo_usuario_var]
        )

        
        nombre_resultado = nombre_var.getvalue()
        codigo_resultado = codigo_usuario_var.getvalue()

       
        if not nombre_resultado and not codigo_resultado:
            raise HTTPException(
                status_code=404,
                detail=error_response("NOT_FOUND", "Propietario no encontrado")
            )

        return {
            "nombre": nombre_resultado, 
            "codigo_usuario": codigo_resultado
        }

    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        conn.rollback() if conn else None
        error, = e.args
        
        # Captura por si Oracle lanza el No Data Found directamente
        if "ORA-01403" in str(error.message):
            raise HTTPException(
                status_code=404,
                detail=error_response("NOT_FOUND", "Propietario no encontrado")
            )
            
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=error_response("INTERNAL_SERVER_ERROR", str(e))
        )
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    
@router.post("", status_code=201)
def create_propietario(prop: Propietarios_create):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        codigo_usuario = cursor.callfunc(
            "PKG_USUARIO.FN_guardar_usuario",
            str,
            [prop.email, hashear_password(prop.contraseña), prop.rol]
        )
        cursor.callproc(
            "PKG_PROPIETARIOS.PRC_GUARDAR", [
            prop.cedula,
            prop.nombreCompleto,
            prop.sexo,
            prop.telefono,
            codigo_usuario
        ])
        conn.commit()
        return {"message": "Propietario creado correctamente."}

    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        # ORA-00001 = unique constraint — cédula o correo duplicado
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

@router.put("/", status_code=200)
def update_propietario( propietario: Propietarios_update, token: dict = Depends(verificar_token)):
    if token["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para actualizar propietarios")
        )

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("PKG_PROPIETARIOS.PRC_ACTUALIZAR", [
            propietario.cedula,
            propietario.nombreCompleto,
            propietario.sexo,
            propietario.telefono
        ])
        conn.commit()
        return {"message": "Propietario actualizado correctamente."}

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

@router.delete("/{propietario_id}", status_code=200)
def delete_propietario(propietario_id: str, token: dict = Depends(verificar_token)):
    if token["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para eliminar propietarios")
        )

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("PKG_PROPIETARIOS.PRC_ELIMINAR", [propietario_id])
        conn.commit()
        return {"message": "Propietario eliminado correctamente."}

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