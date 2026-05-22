from fastapi import APIRouter,HTTPException, Depends
from models.espcies import especies_create, especies_show, especies_update
from database.conexion import get_connection
from utils.token import verificar_token
from utils.error_structure import error_response
import oracledb

router = APIRouter(
    prefix="/especies",
    tags=["especies"]
)   

@router.get("")
def get_especies(token: dict = Depends(verificar_token)):

    if token["rol"] != "1" and token["rol"] != "3":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "Rol no autorizado"))
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        
        datos_cursor = cursor.callfunc("PKG_ESPECIES.FN_CONSULTAR", oracledb.CURSOR, [])
        
        columnas = [col[0].lower() for col in datos_cursor.description]
        especies = []
        for fila in datos_cursor:
            especies.append(especies_show.model_validate(dict(zip(columnas, fila))))
        return especies
        
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

@router.post("", status_code=201)
def create_especie(especie: especies_create,token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "Rol no autorizado"))
    
    try:
        conn   = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_ESPECIES.PRC_GUARDAR", [especie.nombre])
        conn.commit()
        return {"message": "Especie creada correctamente."}
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

@router.put("", status_code=200)
def update_especie(especie: especies_update,token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "Rol no autorizado")
        )

    try:
        conn   = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_ESPECIES.PRC_ACTUALIZAR", [especie.codigo, especie.nombre])
        conn.commit()
        return {"message": "Especie actualizada correctamente."}
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

@router.delete("/{especie_id}", status_code=200)
def delete_especie(especie_id: str, token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(status_code=403, detail=error_response("FORBIDDEN", "Rol no autorizado"))

    try:
        conn   = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_ESPECIES.PRC_ELIMINAR", [especie_id])
        conn.commit()
        return {"message": "Especie eliminada correctamente."}
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
