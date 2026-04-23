from fastapi import APIRouter,HTTPException
from models.consultas import Consultas_create, Consultas_show, Consultas_update
from database.conexion import get_connection
import oracledb
router = APIRouter(
    prefix="/consultas",
    tags=["consultas"]
)

@router.get("")
def get_consultas():
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        
        datos_cursor = cursor.callfunc("PKG_CONSULTAS.FN_CONSULTAR", oracledb.CURSOR, []) 

        if datos_cursor:
            columnas =[col[0].lower() for col in datos_cursor.description]
            consultas =[]
            for fila in datos_cursor:
                dict_fila = dict(zip(columnas,fila))
                consultas.append(Consultas_show(**dict_fila))
            return consultas
        else:
            return[]
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
def create_consulta(consulta: Consultas_create):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        
        cursor.callproc("PKG_CONSULTAS.PRC_GUARDAR", [
            consulta.fecha,
            consulta.descripcion, 
            consulta.diagnostico,
            consulta.tratamiento,
            consulta.codigo_Mascotas,
            consulta.cedula_Veterinario,
            consulta.codigo_cita,
            consulta.codigo_especializacion
        ])
        
        return {"message": "Consulta registrada correctamente."}
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
def update_consulta(consulta: Consultas_update):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_CONSULTAS.PRC_ACTUALIZAR", [
            consulta.id,
            consulta.descripcion,
            consulta.diagnostico,
            consulta.tratamiento
        ])
        
        return {"message": f"Consulta {consulta.id} actualizada correctamente."}
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

@router.delete("/{consulta_id}")
def delete_consulta(consulta_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_CONSULTAS.PRC_ELIMINAR", [consulta_id])
        
        return {"message": "Consulta desactivada correctamente."}
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


