from fastapi import APIRouter, HTTPException
import oracledb
from models.propietarios import Propietarios_create, Propietarios_show, Propietarios_update
from database.conexion import get_connection
from utils.passwordHasser import hashear_password
router = APIRouter(
    prefix="/propietarios",
    tags=["propietarios"]
)

@router.get("")
def get_propietarios():
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        
        datos_cursor =  cursor.callfunc("PKG_PROPIETARIOS.FN_CONSULTAR",oracledb.CURSOR, [])

        if datos_cursor:
            columnas = [col[0].lower() for col in datos_cursor.description]

            propietarios = []
            for fila in datos_cursor:
                dict_fila = dict(zip(columnas,fila))
                propietarios.append(Propietarios_show(**dict_fila))
            return propietarios
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
def create_propietario(prop: Propietarios_create):
    try:
        conn   = get_connection()
        cursor = conn.cursor()

        codigo_usuario = cursor.callfunc("PKG_USUARIO.FN_guardar_usuario",
                                         str,
                                         [prop.email, 
                                          hashear_password(prop.contraseña), 
                                          prop.rol])

        cursor.callproc("PKG_PROPIETARIOS.PRC_GUARDAR",
                        [prop.cedula,
                         prop.nombreCompleto,
                           prop.telefono, 
                           prop.sexo, codigo_usuario])
        
        return {"message": "Propietario creado correctamente."}
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
def update_propietario(propietario: Propietarios_update):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_PROPIETARIOS.PRC_ELIMINAR",
                        [propietario.cedula,
                         propietario.nombreCompleto,
                         propietario.sexo,
                         propietario.telefono])
        
        return {"message": "Propietario actualizado correctamente."}
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

@router.delete("/{propietario_id}")
def delete_propietario(propietario_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_PROPIETARIOS.PRC_ACTUALIZAR",[propietario_id])
        cursor.close()
        conn.close()

        return {"message": "Propietario eliminado correctamente."}
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
