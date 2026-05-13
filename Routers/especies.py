from fastapi import APIRouter,HTTPException, Depends
from models.espcies import especies_create, especies_show, especies_update
from database.conexion import get_connection
from utils.token import verificar_token
import oracledb

router = APIRouter(
    prefix="/especies",
    tags=["especies"]
)

@router.get("")
def get_especies(token: dict = Depends(verificar_token)):

    if token["rol"] != "1" and token["rol"] != "3":
        raise HTTPException(status_code=403, detail="Rol no autorizado")
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        
        datos_cursor = cursor.callfunc("PKG_ESPECIES.FN_CONSULTAR", oracledb.CURSOR, [])

        if datos_cursor:
            columnas = [col[0].lower() for col in datos_cursor.description]

            especies = []
            for fila in datos_cursor:
                dict_fila = dict(zip(columnas, fila))
                especies.append(especies_show(**dict_fila))
            return especies
        else:
            return []

    except HTTPException:
       raise

    except oracledb.DatabaseError as e:
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        raise HTTPException(status_code=500, detail=f"Error en la base de datos {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("")
def create_especie(especie: especies_create,token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(status_code=403, detail="Rol no autorizado")
    
    try:
        conn   = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_ESPECIES.PRC_GUARDAR", [especie.nombre])
        
        return {"message": "Especie creada correctamente."}
    except HTTPException:
       raise

    except oracledb.DatabaseError as e:
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        raise HTTPException(status_code=500, detail=f"Error en la base de datos {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.put("")
def update_especie(especie: especies_update,token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(status_code=403, detail="Rol no autorizado")

    try:
        conn   = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_ESPECIES.PRC_ACTUALIZAR", [especie.codigo, especie.nombre])
        
        return {"message": "Especie actualizada correctamente."}
    except HTTPException:
       raise

    except oracledb.DatabaseError as e:
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        raise HTTPException(status_code=500, detail=f"Error en la base de datos {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.delete("/{especie_id}")
def delete_especie(especie_id: str, token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(status_code=403, detail="Rol no autorizado")

    try:
        conn   = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_ESPECIES.PRC_ELIMINAR", [especie_id])
        
        return {"message": "Especie eliminada correctamente."}
    except HTTPException:
       raise

    except oracledb.DatabaseError as e:
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        raise HTTPException(status_code=500, detail=f"Error en la base de datos {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

