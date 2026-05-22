from fastapi import APIRouter, HTTPException, Depends
from models.especializaciones import Especializaciones_create, Especializaciones_show, Especializaciones_update
from database.conexion import get_connection
from utils.token import verificar_token
from utils.error_structure import error_response    
import oracledb

router = APIRouter(
    prefix="/especializaciones",
    tags=["especializaciones"]
)   


@router.get("")
def get_especializaciones(token: dict = Depends(verificar_token)):
    
    if token["rol"] != "1" and token["rol"] != "2" and token["rol"] != "3":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para ver las especializaciones")
        )

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor_result = cursor.callfunc(
            "PKG_ESPECIALIZACIONES.FN_CONSULTAR",
            oracledb.CURSOR
        )
    
        columnas = [col[0].lower() for col in cursor_result.description]
        datos = []
        for fila in cursor_result:
            datos.append(Especializaciones_show.model_validate(dict(zip(columnas,fila))))
        return datos
    except HTTPException:
       raise
    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail=error_response("UNAUTHORIZED", "Credenciales incorrectas"))
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", f"Error en la base de datos {e}"))
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", str(e)))
    finally:
        cursor.close()
        conn.close()

@router.post("", status_code=201)
def create_especializacion(especializacion: Especializaciones_create, token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para crear especializaciones")
        )
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.callproc(
            "PKG_ESPECIALIZACIONES.PRC_GUARDAR",
            [especializacion.nombre]
        )
        conn.commit()
        return {"message": "Especialización creada exitosamente"}

    except HTTPException:
       raise

    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail=error_response("UNAUTHORIZED", "Credenciales incorrectas"))
        else:
            raise HTTPException(status_code=500, detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}]))
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", str(e)))
    finally:
        cursor.close()
        conn.close()


@router.put("", status_code=200)
def update_especializacion(especializacion: Especializaciones_update, token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para actualizar especializaciones")
        )

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.callproc(
            "PKG_ESPECIALIZACIONES.PRC_ACTUALIZAR",
            [especializacion.codigo, especializacion.nombre]
        )
        conn.commit()
        return {"message": "Especialización actualizada exitosamente"}

    except HTTPException:
       raise

    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail=error_response("UNAUTHORIZED", "Credenciales incorrectas"))
        else:
            raise HTTPException(status_code=500, detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}]))
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", str(e)))
    finally:
        cursor.close()
        conn.close()


@router.delete("/{especializacion_id}", status_code=200)
def delete_especializacion(especializacion_id: str, token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para eliminar especializaciones")
        )
    
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc(
            "PKG_ESPECIALIZACIONES.PRC_ELIMINAR",
            [especializacion_id]
        )
        conn.commit()
        return {"message":"Especialización eliminada exitosamente"}

    except HTTPException:
       raise

    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail=error_response("UNAUTHORIZED", "Credenciales incorrectas"))
        raise HTTPException(status_code=500, detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}]))
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", str(e)))
    finally:
        cursor.close()
        conn.close()    