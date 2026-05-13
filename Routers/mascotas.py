from fastapi import APIRouter, File, UploadFile,HTTPException, Depends
from models.mascotas import Masotas_create, Mascotas_show, Mascotas_update
from database.conexion import get_connection
from utils.cloudinary import subir_imagen
from utils.token import verificar_token
import oracledb

router = APIRouter(
    prefix="/mascotas",
    tags=["mascotas"]
)

@router.get("")
def get_mascotas(token: dict = Depends(verificar_token)):

    if token["rol"] != "1":
        raise HTTPException(status_code=403, detail="Rol no autorizado")
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor_result = cursor.callfunc(
            "PKG_MASCOTAS.FN_CONSULTAR",
            oracledb.CURSOR
        )
        if cursor_result:

            columnas = [col[0].lower() for col in cursor_result.description]
            mascotas = []
            for fila in cursor_result:
                dict_fila = dict(zip(columnas,fila))
                mascotas.append(Mascotas_show(**dict_fila))
            return mascotas
        else:
            return[]

    except oracledb.DatabaseError as e:
        error, = e.args
        raise HTTPException(status_code=500, detail=str(error.message))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

@router.post("")
def create_mascota(mascota: Masotas_create,token: dict = Depends(verificar_token)):

    if token["rol"] != "1" and token["rol"]!= "3":
        raise HTTPException(status_code=403, detail="Rol no autorizado")

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
        raise HTTPException(status_code=500, detail=f"Error al guardar mascota: {e}")
    finally:
        cursor.close()
        conn.close()


@router.get("/propietario/{codigo_usuario}")
def get_mascotas_by_propietario(codigo_usuario: str,token: dict = Depends(verificar_token)):
    if token["rol"] != "3":
        raise HTTPException(status_code=403, detail="Rol no autorizado")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor_result = cursor.callfunc(
            "PKG_MASCOTAS.FN_CONSULTAR_POR_PROPIETARIO",
            oracledb.CURSOR,
            [codigo_usuario]
        )

        columnas = [col[0].lower() for col in cursor_result.description]
        mascotas = []
        for fila in cursor_result:
            mascotas.append(dict(zip(columnas, fila)))
        return mascotas

    except oracledb.DatabaseError as e:
        error, = e.args
        raise HTTPException(status_code=500, detail=str(error.message))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

@router.put("/{codigo_mascota}")
def update_mascota(codigo_mascota: str, mascota: Mascotas_update,token: dict = Depends(verificar_token)):

    if token["rol"] != "3" and token["rol"] != "1":
        raise HTTPException(status_code=403, detail="Rol no autorizado")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_MASCOTAS.PRC_ACTUALIZAR", [
            codigo_mascota,
            mascota.nombre,
            mascota.codigo_especie,
            mascota.codigo_raza
        ])
        
        
        return {"message": f"Mascota {codigo_mascota} actualizada correctamente."}
    
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

@router.delete("/{mascota_id}")
def delete_mascota(mascota_id: str, token: dict = Depends(verificar_token)):
    if token["rol"] != "3" and token["rol"]!="1":
        raise HTTPException(status_code=403, detail="Rol no autorizado")
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_MASCOTAS.PRC_ELIMINAR", [mascota_id])
        
        return {"message": "Mascota eliminada correctamente."}
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


@router.post("/imagenes")
async def upload_image(file: UploadFile = File(...),token: dict = Depends(verificar_token)):
    if token["rol"] != "3":
        raise HTTPException(status_code=403, detail="Rol no autorizado")
    
    try:
       
        res_cloudinary = subir_imagen(file.file, "mascotas")
        
        url = res_cloudinary["url"]

        return {
                "message": "Imagen guardada",
                "url": url
                }

    except Exception as e:
        # ESTO es lo que nos dirá la verdad en el navegador
        raise HTTPException(status_code=500, detail=str(e)) # Esto lo verás en el F12



