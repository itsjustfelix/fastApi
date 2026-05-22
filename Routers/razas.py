from fastapi import APIRouter,HTTPException, Depends
from models.razas import Razas_create, Razas_show, Razas_update,Razas_option
from database.conexion import get_connection
from utils.token import verificar_token
from utils.error_structure import error_response
import oracledb
router = APIRouter(
    prefix="/razas",
    tags=["razas"]
)

@router.get("")
def get_razas(token: dict = Depends(verificar_token)):
    if token["rol"] != "1" and token["rol"] != "3":
        raise HTTPException(status_code=403, detail=error_response("FORBIDDEN", "Rol no autorizado"))
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor_result = cursor.callfunc(
            "PKG_RAZAS.FN_CONSULTAR",
            oracledb.CURSOR
        )

        columnas = [col[0].lower() for col in cursor_result.description]
        razas = []
        for fila in cursor_result:
            razas.append(Razas_show.model_validate(dict(zip(columnas,fila))))
        return razas
        
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

@router.get("/especie/{codigo_especie}")
def get_razas_by_especie(codigo_especie: str,token: dict = Depends(verificar_token)):

    if token["rol"] != "1" and token["rol"] != "3":
        raise HTTPException(status_code=403, detail=error_response("FORBIDDEN", "Rol no autorizado"))
    try:
        conn = get_connection()
        cursor = conn.cursor()

        datos_cursor = cursor.callfunc("PKG_RAZAS.fn_buscar_por_especie", 
                                       oracledb.CURSOR, 
                                       [codigo_especie])
        
        columnas = [col[0].lower() for col in datos_cursor.description]
        razas = []
        for fila in datos_cursor:
            razas.append(Razas_option.model_validate(dict(zip(columnas, fila))))
        return razas

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

@router.post("",status_code=201)
def create_raza(raza: Razas_create,token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(
            status_code=403, 
            detail=error_response("FORBIDDEN", "Rol no autorizado")
        )

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_RAZAS.PRC_GUARDAR", [
            raza.nombre,
            raza.codigo_especie
        ])
        conn.commit()
        return {"message": "Raza creada correctamente."}
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
def update_raza(raza: Razas_update, token: dict = Depends(verificar_token)):
    if token["rol"] != "1":
        raise HTTPException(
            status_code=403, 
            detail=error_response("FORBIDDEN", "Rol no autorizado")
        )
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_RAZAS.PRC_ACTUALIZAR", [
            raza.codigo,
            raza.nombre,
            raza.codigo_especie
        ])
        conn.commit()
        return {"message": "Raza actualizada correctamente."}
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

@router.delete("/{raza_id}")
def delete_raza(raza_id: str, token: dict = Depends(verificar_token)):
    if token["rol"] != "1":
        raise HTTPException(status_code=403, detail=error_response("FORBIDDEN", "Rol no autorizado"))
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_RAZAS.PRC_ELIMINAR", [raza_id])
        conn.commit()
        return {"message": "Raza desactivada correctamente."}
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

