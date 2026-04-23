from fastapi import APIRouter,HTTPException
from models.veterinarios import Veterinarios_create, Veterinarios_show, Veterinarios_update
from database.conexion import get_connection
from utils.passwordHasser import hashear_password
import oracledb
router = APIRouter(
    prefix="/veterinarios",
    tags=["veterinarios"]
)

@router.get("")
def get_veterinarios():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor_result = cursor.callfunc(
            "PKG_VETERINARIOS.FN_CONSULTAR",
            oracledb.CURSOR
        )

        columnas = [col[0].lower() for col in cursor_result.description]
        veterinarios = []
        for fila in cursor_result:
            veterinarios.append(dict(zip(columnas, fila)))
        return veterinarios

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
def create_veterinario(veterinario: Veterinarios_create):
    try:
        conn   = get_connection()
        cursor = conn.cursor()

        v_codigo_usuario = cursor.callfunc("PKG_USUARIO.FN_guardar_usuario",
                                         str,
                                         [veterinario.email, 
                                          hashear_password(veterinario.contraseña), 
                                          veterinario.rol])


        cursor.callproc("PKG_VETERINARIOS.PRC_GUARDAR", [
            veterinario.cedula,
            veterinario.nombreCompleto,
            veterinario.sexo,
            veterinario.telefono,
            veterinario.codigo_especialidad,
            v_codigo_usuario
        ])
        
        return {"message": "Veterinario creado correctamente."}
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
def update_veterinario(veterinario: Veterinarios_update):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_VETERINARIOS.PRC_ACTUALIZAR", [
            veterinario.cedula,
            veterinario.nombreCompleto,
            veterinario.sexo,
            veterinario.telefono,
            veterinario.codigo_especialidad
        ])
        
        return {"message": "Veterinario  actualizado correctamente."}
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

@router.delete("/{veterinario_id}")
def delete_veterinario(veterinario_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_VETERINARIOS.PRC_ELIMINAR", [veterinario_id])
        
        return {"message": "Veterinario desactivado correctamente."}
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

