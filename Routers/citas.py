from fastapi import APIRouter, HTTPException, Depends
from models.citas import Citas_create, Citas_show,Citas_show_veterinario, Citas_update
from database.conexion import get_connection
from utils.token import verificar_token
from utils.error_structure import error_response
import oracledb

router = APIRouter(
    prefix="/citas",
    tags=["citas"]
)

@router.get("")
def get_citas(token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(
            status_code=403, 
            detail=error_response("FORBIDDEN", "No autorizado para ver citas")
        )
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        datos_cursor = cursor.callfunc(
            "PKG_CITAS.FN_CONSULTAR",
            oracledb.CURSOR,
            []
        )

        columnas = [col[0].lower() for col in datos_cursor.description]
        citas = []
        for fila in datos_cursor:
            citas.append(Citas_show.model_validate(dict(zip(columnas,fila))))
        return citas
    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        error, = e.args
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("SERVER_ERROR", "Error interno del servidor", [{"message": str(e)}])
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/propietario/{codigo_usuario}")
def get_citas_by_codigo_usuario(codigo_usuario: str,token: dict = Depends(verificar_token) ):
    
    if token["rol"] != "3":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para ver las citas")
        )

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor_result = cursor.callfunc(
            "PKG_CITAS.FN_BUSCAR_POR_CODIGO_USUARIO",
            oracledb.CURSOR,   
            [codigo_usuario]    
        )

        columnas = [col[0].lower() for col in cursor_result.description]
        citas = []
        for fila in cursor_result:
            citas.append(Citas_show.model_validate(dict(zip(columnas, fila))))
        return citas

    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        error, = e.args
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("SERVER_ERROR", "Error interno del servidor", [{"message": str(e)}])
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/veterinario/{cedula_veterinario}")
def get_citas_by_cedula_veterinario(cedula_veterinario: str, token: dict = Depends(verificar_token)):

    if token["rol"] != "2":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para ver citas")
        )

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor_result = cursor.callfunc(
            "PKG_CITAS.FN_BUSCAR_POR_CEDULA_VETERINARIO",
            oracledb.CURSOR,
            [cedula_veterinario]
        )

        columnas = [col[0].lower() for col in cursor_result.description]
        citas = []
        for fila in cursor_result:
            citas.append(Citas_show_veterinario.model_validate(dict(zip(columnas, fila))))
        return citas

    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        error, = e.args
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("SERVER_ERROR", "Error interno del servidor", [{"message": str(e)}])
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/ocupadas")
def get_citas_ocupadas(cedula_veterinario: str, fecha: str, token: dict = Depends(verificar_token)):

    if token["rol"] != "2" and token["rol"] != "1" and token["rol"] != "3":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para ver las horas ocupadas", [token["rol"]])
    )

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor_result = cursor.callfunc(
            "PKG_CITAS.fn_obtener_horas_ocupadas",
            oracledb.CURSOR,
            [cedula_veterinario, fecha]
        )

        columnas = [col[0].lower() for col in cursor_result.description]
        horas = []
        for fila in cursor_result:
            dato = dict(zip(columnas, fila))
            horas.append(dato["hora"])
        return horas

    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        error, = e.args
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=error_response("SERVER_ERROR", "Error interno del servidor", [{"message": str(e)}])
        )
    finally:
        cursor.close()
        conn.close()



@router.post("", status_code=201)
def create_cita(cita: Citas_create,token: dict = Depends(verificar_token)):

    if  token["rol"] != "1" and token["rol"] != "3":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para crear citas")
        )
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc(
            "PKG_CITAS.PRC_GUARDAR", [
            cita.fecha,
            cita.hora,
            cita.codigoMascota,
            cita.cedulaVeterinario,
            cita.codigoEspecializacion
        ])
        conn.commit()
        return {"message": "Cita creada correctamente."}
    except HTTPException:
       raise

    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail=error_response("UNAUTHORIZED", "Credenciales incorrectas"))
        else:   
            raise HTTPException(status_code=500, detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}]))

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", str(e)))

    finally:
        cursor.close()
        conn.close()

@router.put("", status_code=200)
def update_cita(cita: Citas_update,token: dict = Depends(verificar_token)):

    if  token["rol"] != "1" and token["rol"] != "3":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para actualizar citas")
        )

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_CITAS.PRC_ACTUALIZAR", [
            cita.codigo,
            cita.fecha,
            cita.hora
        ])
        conn.commit()
        return {"message": "Cita actualizada correctamente."}
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

@router.delete("/{cita_id}", status_code=200)
def delete_cita(cita_id: str,token: dict = Depends(verificar_token)):

    if token["rol"] != "3" and token["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para eliminar citas")
        )

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_CITAS.PRC_ELIMINAR",[cita_id])
        conn.commit()
        
        return {"message": "Cita cancelada correctamente."}
    except HTTPException:
       raise
    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        if "ORA-20002" in str(error.message):
            raise HTTPException(status_code=401, detail=error_response("UNAUTHORIZED", "Credenciales incorrectas"))
        else:
            raise HTTPException(status_code=500, detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}]))

    finally:
        cursor.close()
        conn.close()
