from fastapi import APIRouter,HTTPException, Depends
from models.veterinarios import Veterinarios_create, Veterinarios_show, Veterinarios_update,Veterinarios_show_option
from database.conexion import get_connection
from utils.passwordHasser import hashear_password
from utils.token import verificar_token
from utils.error_structure import error_response
import oracledb

router = APIRouter(
    prefix="/veterinarios",
    tags=["veterinarios"]
)

@router.get("")
def get_veterinarios(token: dict = Depends(verificar_token)):
    if token["rol"] != "1" and token["rol"]!= "3":
        raise HTTPException(status_code=403, detail=error_response("FORBIDDEN", "Rol no autorizado"))
    
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
            veterinarios.append(Veterinarios_show.model_validate(dict(zip(columnas,fila))))
        return veterinarios
    except HTTPException:
       raise
    except oracledb.DatabaseError as e:
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(
                status_code=401,
                detail=error_response("UNAUTHORIZED", "Credenciales incorrectas")
            )
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", str(e)))
    finally:
        cursor.close()
        conn.close()

@router.get("/option")
def get_veterinario_option(token: dict = Depends(verificar_token)):
    
    if token["rol"] != "1" and token["rol"] != "3":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "Rol no autorizado")
        )
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor_result = cursor.callfunc(
            "PKG_VETERINARIOS.FN_CONSULTAR_OPTION",
            oracledb.CURSOR
        )

        columnas = [col[0].lower() for col in cursor_result.description]
        veterinarios = []
        for fila in cursor_result:
            veterinarios.append(Veterinarios_show_option.model_validate(dict(zip(columnas, fila))))
        return veterinarios

    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        error, = e.args
        raise HTTPException(status_code=500, detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}]))
    except Exception as e:
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", str(e)))
    finally:
        cursor.close()
        conn.close()

@router.post("",status_code=201)
def create_veterinario(veterinario: Veterinarios_create,token: dict = Depends(verificar_token)):
    if token["rol"] != "1":
        raise HTTPException(status_code=403, detail=error_response("FORBIDDEN", "Rol no autorizado para crear veterinarios"))
    try:

        conn   = get_connection()
        cursor = conn.cursor()

        v_codigo_usuario = cursor.callfunc(
            "PKG_USUARIO.FN_guardar_usuario",
            str,
            [veterinario.email, 
            hashear_password(veterinario.contraseña), 
            veterinario.rol])


        cursor.callproc(
            "PKG_VETERINARIOS.PRC_GUARDAR",[
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
            raise HTTPException(status_code=401, detail=error_response("UNAUTHORIZED", "Credenciales incorrectas"))
        raise HTTPException(status_code=500, detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}]))
    except Exception as e:
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", str(e)))
    finally:
        cursor.close()
        conn.close()

@router.put("",status_code=200)
def update_veterinario(veterinario: Veterinarios_update,token: dict = Depends(verificar_token)):
    if token["rol"] != "1":
        raise HTTPException(status_code=403, detail=error_response("FORBIDDEN", "Rol no autorizado"))   
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
            raise HTTPException(status_code=401, detail=error_response("UNAUTHORIZED", "Credenciales incorrectas"))
        raise HTTPException(status_code=500, detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}]))
    except Exception as e:
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", str(e)))
    finally:
        cursor.close()
        conn.close()

@router.delete("/{veterinario_id}",status_code=200)
def delete_veterinario(veterinario_id: str,token: dict = Depends(verificar_token)):
    if token["rol"] != "1":
        raise HTTPException(status_code=403, detail=error_response("FORBIDDEN", "Rol no autorizado"))
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
            raise HTTPException(status_code=401, detail=error_response("UNAUTHORIZED", "Credenciales incorrectas"))
        raise HTTPException(status_code=500, detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}]))
    except Exception as e:
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", str(e)))
    finally:
        cursor.close()
        conn.close()

