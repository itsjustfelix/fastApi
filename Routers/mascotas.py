from fastapi import APIRouter, File, UploadFile,HTTPException, Depends
from models.mascotas import Mascotas_create, Mascotas_show, Mascotas_update
from database.conexion import get_connection
from utils.cloudinary import subir_imagen
from utils.token import verificar_token
from utils.error_structure import error_response
import oracledb

router = APIRouter(
    prefix="/mascotas",
    tags=["mascotas"]
)


@router.get("")
def get_mascotas(token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(
            status_code=403, 
            detail=error_response("FORBIDDEN", "Rol no autorizado")
        )
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor_result = cursor.callfunc(
            "PKG_MASCOTAS.FN_CONSULTAR",
            oracledb.CURSOR
        )
        
        columnas = [col[0].lower() for col in cursor_result.description]
        mascotas = []
        for fila in cursor_result:
            mascotas.append(Mascotas_show.model_validate(dict(zip(columnas,fila))))
        return mascotas
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

@router.get("/propietario/{codigo_usuario}")
def get_mascotas_by_propietario(codigo_usuario: str,token: dict = Depends(verificar_token)):
    if token["rol"] != "3":
        raise HTTPException(status_code=403, detail=error_response("FORBIDDEN", "Rol no autorizado"))
    
    
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor_result = cursor.callfunc(
            "PKG_MASCOTAS.FN_CONSULTAR_POR_PROPIETARIO",
            oracledb.CURSOR,
            [codigo_usuario]
        )

        columnas = [col[0].lower() for col in cursor_result.description]
        mascotas = []
        for fila in cursor_result:
            mascotas.append(Mascotas_show.model_validate(dict(zip(columnas, fila))))
        return mascotas

    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        raise HTTPException(status_code=500, detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}]))

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", str(e)))

    finally:
        cursor.close()
        conn.close()

@router.post("",status_code=201)
def create_mascota(mascota: Mascotas_create,token: dict = Depends(verificar_token)):

    if token["rol"] != "1" and token["rol"]!= "3":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "Rol no autorizado"))
    try:
        conn   = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_MASCOTAS.PRC_GUARDAR", [
            mascota.nombre,
            mascota.codigo_especie,
            mascota.codigo_raza,
            mascota.codigo_propietario,
            mascota.link_imagen
        ])
        
        return {"message": "Mascota creada correctamente."}
    except oracledb.DatabaseError as e:
        conn.rollback()
        error, = e.args
        raise HTTPException(status_code=500, detail=error_response("DATABASE_ERROR", "Error en la base de datos", [{"message": str(error.message)}]))
    finally:
        cursor.close()
        conn.close()

@router.put("/{codigo_mascota}",status_code=200)
def update_mascota(codigo_mascota: str, mascota: Mascotas_update,token: dict = Depends(verificar_token)):

    if token["rol"] != "3" and token["rol"] != "1":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "Rol no autorizado"))

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_MASCOTAS.PRC_ACTUALIZAR", [
            codigo_mascota,
            mascota.nombre,
            mascota.codigo_especie,
            mascota.codigo_raza
        ])
        
        return {"message":"Mascota actualizada correctamente."}
    
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

@router.delete("/{mascota_id}", status_code=200)
def delete_mascota(mascota_id: str, token: dict = Depends(verificar_token)):
    if token["rol"] != "3" and token["rol"]!="1":
        raise HTTPException(
            status_code=403, 
            detail=error_response("FORBIDDEN", "Rol no autorizado")
        )
    
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_MASCOTAS.PRC_ELIMINAR", [mascota_id])
        
        return {"message": "Mascota eliminada correctamente."}
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

@router.post("/imagenes")
async def upload_image(file: UploadFile = File(...),token: dict = Depends(verificar_token)):
    if token["rol"] != "3":
        raise HTTPException(
            status_code=403,
            detail=error_response("FORBIDDEN", "Rol no autorizado")
        )
    try:
        res_cloudinary = subir_imagen(file.file, "mascotas")
        url = res_cloudinary["url"]
        return {
                "message": "Imagen guardada",
                "url": url
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=error_response("INTERNAL_SERVER_ERROR", str(e)))
