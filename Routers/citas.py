from fastapi import APIRouter, HTTPException
from models.citas import Citas_create, Citas_show, Citas_update
from database.conexion import get_connection
import oracledb

router = APIRouter(
    prefix="/citas",
    tags=["citas"]
)

@router.get("")
def get_citas():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        datos_cursor = cursor.callfunc("PKG_CITAS.FN_CONSULTAR", oracledb.CURSOR, [])

        if datos_cursor:
            columnas = [col[0].lower() for col in datos_cursor.description]
            citas = []
            for fila in datos_cursor:
                dict_fila = dict(zip(columnas,fila))
                citas.append(Citas_show(**dict_fila))
            return citas
        else:
            return []

    except HTTPException:
       raise

    except oracledb.DatabaseError as e:
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        raise HTTPException(status_code=500, detail="Error en la base de datos")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
    

@router.get("/propietario/{codigo_usuario}")
def get_citas_by_codigo_usuario(codigo_usuario: str):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        
        cursor_result = cursor.callfunc(
            "PKG_CITAS.FN_BUSCAR_POR_CODIGO_USUARIO",
            oracledb.CURSOR,   
            [codigo_usuario]    
        )

        columnas = [col[0].lower() for col in cursor_result.description]
        citas = []
        for fila in cursor_result:
            citas.append(dict(zip(columnas, fila)))
        return citas

    except HTTPException:
        raise

    except oracledb.DatabaseError as e:
        error, = e.args
        raise HTTPException(status_code=500, detail=f"Error en la base de datos {error.message}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


@router.post("")
def create_cita(cita: Citas_create):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_CITAS.PRC_GUARDAR", [
            cita.fecha,
            cita.hora,
            cita.codigoMascota,
            cita.cedulaVeterinario
        ])
        
        return {"message": "Cita creada correctamente."}
    except HTTPException:
       raise

    except oracledb.DatabaseError as e:
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        raise HTTPException(status_code=500, detail="Error en la base de datos")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


@router.put("")
def update_cita(cita: Citas_update):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_CITAS.PRC_ACTUALIZAR", [
            cita.codigo,
            cita.fecha,
            cita.hora
        ])
        
        return {"message": "Cita actualizada correctamente."}
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


@router.delete("/{cita_id}")
def delete_cita(cita_id: int):   
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_CITAS.PRC_ELIMINAR", [cita_id])
        
        return {"message": "Cita cancelada correctamente."}
    except HTTPException:
       raise

    except oracledb.DatabaseError as e:
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        raise HTTPException(status_code=500, detail="Error en la base de datos")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

