from fastapi import APIRouter, HTTPException, Depends
from models.especializaciones import Especializaciones_create, Especializaciones_show, Especializaciones_update
from database.conexion import get_connection
from utils.token import verificar_token
import oracledb

router = APIRouter(
    prefix="/especializaciones",
    tags=["especializaciones"]
)

@router.get("")
def get_especializaciones(token: dict = Depends(verificar_token)):
    
    if token["rol"] != "1" and token["rol"] != "2" and token["rol"] != "3":
        raise HTTPException(status_code=403, detail="Rol no autorizado")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor_result = cursor.callfunc(
            "PKG_ESPECIALIZACIONES.FN_CONSULTAR",
            oracledb.CURSOR
        )
        if cursor_result:
            columnas = [col[0].lower() for col in cursor_result.description]
            datos = []
            for fila in cursor_result:
                dict_fila = dict(zip(columnas,fila))
                datos.append(Especializaciones_show(**dict_fila))
        return datos

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
def create_especializacion(especializacion: Especializaciones_create, token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(status_code=403, detail="Rol no autorizado")
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc(
            "PKG_ESPECIALIZACIONES.PRC_GUARDAR",
            [especializacion.nombre]
        )
        return {"message": "Especialización creada exitosamente"}

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


@router.put("/")
def update_especializacion(especializacion: Especializaciones_update, token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(status_code=403, detail="Rol no autorizado")

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
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        raise HTTPException(status_code=500, detail=f"Error en la base de datos {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.delete("/{especializacion_id}")
def delete_especializacion(especializacion_id: str, token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(status_code=403, detail="Rol no autorizado")
    
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
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        raise HTTPException(status_code=500, detail=f"Error en la base de datos {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()