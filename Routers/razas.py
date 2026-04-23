from fastapi import APIRouter,HTTPException
from models.razas import Razas_create, Razas_show, Razas_update
from database.conexion import get_connection
import oracledb
router = APIRouter(
    prefix="/razas",
    tags=["razas"]
)

@router.get("")
def get_razas():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor_result = cursor.callfunc(
            "PKG_RAZAS.FN_CONSULTAR",
            oracledb.CURSOR
        )

        columnas = [col[0].lower() for col in cursor_result.description]
        razas = []
        for fila in cursor_result:
            razas.append(dict(zip(columnas, fila)))
        return razas

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
def create_raza(raza: Razas_create):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_RAZAS.PRC_GUARDAR", [
            raza.nombre,
            raza.codigo_especie
        ])
        
        return {"message": "Raza creada correctamente."}
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

    
@router.get("/especie/{codigo_especie}")
def get_razas_by_especie(codigo_especie: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        datos_cursor = cursor.callfunc("PKG_RAZAS.FN_BUSCAR_POR_ESPECIE", 
                                       oracledb.CURSOR, 
                                       [codigo_especie])
        
        if datos_cursor:
            columnas = [col[0].lower() for col in datos_cursor.description]
            razas = []
            for fila in datos_cursor:
                dict_fila = dict(zip(columnas, fila))
                razas.append(Razas_show(
                    codigo=dict_fila['codigo'],
                    nombre=dict_fila['nombre'],
                    especie=dict_fila['nombre_especie']
                ))
            return razas
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

@router.put("")
def update_raza(raza: Razas_update):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_RAZAS.PRC_ACTUALIZAR", [
            raza.codigo,
            raza.nombre,
            raza.codigo_especie
        ])
        
        return {"message": "Raza actualizada correctamente."}
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

@router.delete("/{raza_id}")
def delete_raza(raza_id: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_RAZAS.PRC_ELIMINAR", [raza_id])
        
        return {"message": "Raza desactivada correctamente."}
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

