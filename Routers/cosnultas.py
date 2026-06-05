from fastapi import APIRouter,HTTPException, Depends, Response
from models.consultas import Consultas_create, Consultas_show, Consultas_update
from database.conexion import get_connection
from utils.token import verificar_token
from utils.error_structure import error_response
from utils.creador_documento import crear_documento_pdf
import oracledb
router = APIRouter(
    prefix="/consultas",
    tags=["consultas"]
)

@router.get("")
def get_consultas(token: dict = Depends(verificar_token)):

    if token["rol"] != "1" and token["rol"] != "2":
        raise HTTPException(
            status_code=403, 
            detail=error_response("FORBIDDEN", "No autorizado para ver las consultas")
        )
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        datos_cursor = cursor.callfunc("PKG_CONSULTAS.FN_CONSULTAR", oracledb.CURSOR, [])
    
        columnas =[col[0].lower() for col in datos_cursor.description]
        consultas =[]
        for fila in datos_cursor:
            consultas.append(Consultas_show.model_validate(dict(zip(columnas,fila))))
            
        return consultas
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
def get_consulta_by_codigo_propietario(codigo_usuario: str,token: dict = Depends(verificar_token)):

    if token["rol"] != "3" and token ["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para actualizar las consultas")
        )
    
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        
        datos_cursor = cursor.callfunc("PKG_CONSULTAS.fn_consultar_por_codigo_propietario", oracledb.CURSOR,[codigo_usuario]) 

        columnas =[col[0].lower() for col in datos_cursor.description]
        consultas =[]
        for fila in datos_cursor:
            consultas.append(Consultas_show.model_validate(dict(zip(columnas,fila))))
        return consultas
      
    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=error_response("SERVER_ERROR", "Error interno del servidor", [{"message": str(e)}])
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/veterinario/{codigo_veterinario}")
def get_consulta_by_codigo_veterinario(codigo_veterinario: str,token: dict = Depends(verificar_token)):

    if token["rol"] != "2":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para actualizar las consultas")
        )
    
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        
        datos_cursor = cursor.callfunc("PKG_CONSULTAS.fn_consultar_por_codigo_veterinario", oracledb.CURSOR,[codigo_veterinario]) 

        columnas =[col[0].lower() for col in datos_cursor.description]
        consultas =[]
        for fila in datos_cursor:
            consultas.append(Consultas_show.model_validate(dict(zip(columnas,fila))))
        return consultas
      
    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=error_response("SERVER_ERROR", "Error interno del servidor", [{"message": str(e)}])
        )
    finally:
        cursor.close()
        conn.close()

@router.get("/mascota/{codigo_mascota}")
def get_consulta_by_codigo_mascota(codigo_mascota: str,token: dict = Depends(verificar_token)):

    if token["rol"] != "3" and token ["rol"] != "2":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para actualizar las consultas")
        )
    
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        
        datos_cursor = cursor.callfunc("PKG_CONSULTAS.fn_consultar_por_codigo_mascota", oracledb.CURSOR,[codigo_mascota]) 

        columnas =[col[0].lower() for col in datos_cursor.description]
        consultas =[]
        for fila in datos_cursor:
            consultas.append(Consultas_show.model_validate(dict(zip(columnas,fila))))
        return consultas
      
    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=error_response("SERVER_ERROR", "Error interno del servidor", [{"message": str(e)}])
        )
    finally:
        cursor.close()
        conn.close()


@router.post("",status_code=201)
def create_consulta(consulta: Consultas_create,token: dict = Depends(verificar_token)):

    if token["rol"] != "2":
        raise HTTPException(
            status_code=403,
            detail= error_response("FORBIDDEN", "No autorizado para crear las consultas")
        )
    
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc(
            "PKG_CONSULTAS.PRC_GUARDAR", [
            consulta.fecha,
            consulta.descripcion, 
            consulta.diagnostico,
            consulta.tratamiento,
            consulta.codigo_Mascotas,
            consulta.cedula_Veterinario,
            consulta.codigo_cita,
            consulta.codigo_especializacion
        ])
        conn.commit()
        return {"message": "Consulta registrada correctamente."}
    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=error_response("SERVER_ERROR", "Error interno del servidor", [{"message": str(e)}])
        )
    finally:
        cursor.close()
        conn.close()

@router.put("")
def update_consulta(consulta: Consultas_update, token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para actualizar las consultas")
            )

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc(
            "PKG_CONSULTAS.PRC_ACTUALIZAR", [
            consulta.id,
            consulta.descripcion,
            consulta.diagnostico,
            consulta.tratamiento
        ])
        conn.commit()
        return {"message": "Consulta actualizada correctamente."}
    except HTTPException:
        raise
    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        raise HTTPException(
            status_code=500,
            detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}])
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=error_response("SERVER_ERROR", "Error interno del servidor", [{"message": str(e)}])
        )
    finally:
        cursor.close()
        conn.close()

@router.delete("/{consulta_id}")
def delete_consulta(consulta_id: str,token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para eliminar las consultas")
        )

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_CONSULTAS.PRC_ELIMINAR", [consulta_id])
        conn.commit()
        return {"message": "Consulta desactivada correctamente."}
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


@router.get("/pdf/{consulta_id}")
def get_consulta_pdf(consulta_id: str, token: dict = Depends(verificar_token)):
    if token["rol"] != "3" and token["rol"] != "2" and token["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "No autorizado para descargar el PDF de la consulta")
        )
    
    try:
        conn = get_connection()
        cursor = conn.cursor()

        data_cursor = cursor.callfunc("PKG_CONSULTAS.fn_consultar_por_codigo", oracledb.CURSOR, [consulta_id])

        columnas = [col[0].lower() for col in data_cursor.description]

        fila = data_cursor.fetchone()
        if not fila:
            raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", "Consulta no encontrada"))
        
        consulta_data = Consultas_show.model_validate(dict(zip(columnas, fila)))

        pdf_bytes = crear_documento_pdf(consulta_data)

        return Response(
            content=pdf_bytes, 
            media_type="application/pdf", 
            headers={"Content-Disposition": f"attachment; filename=consulta_{consulta_id}.pdf"}
        )    
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