from fastapi import APIRouter, File, UploadFile,HTTPException
from models.mascotas import Masotas_create, Mascotas_show, Mascotas_update
from database.conexion import get_connection
import oracledb
from utils.cloudinary import subir_imagen
router = APIRouter(
    prefix="/mascotas",
    tags=["mascotas"]
)

@router.get("")
def get_mascotas():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor_result = cursor.callfunc(
            "PKG_MASCOTAS.FN_CONSULTAR",
            oracledb.CURSOR
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

@router.post("")
def create_mascota(mascota: Masotas_create):
    try:
        conn   = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_MASCOTAS.PRC_GUARDAR", [
            mascota.nombre,
            mascota.codigo_especie,
            mascota.codigo_raza,
            mascota.codigo_propietario,
            mascota.codigo_imagen
        ])
        
        return {"message": "Mascota creada correctamente."}
    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar mascota: {e}")
    finally:
        cursor.close()
        conn.close()


@router.get("/propietario/{codigo_usuario}")
def get_mascotas_by_propietario(codigo_usuario: str):
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

@router.put("")
def update_mascota(mascota: Mascotas_update):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("PKG_MASCOTAS.PRC_ACTUALIZAR", [
            mascota.codigo,
            mascota.nombre,
            mascota.codigo_especie,
            mascota.codigo_raza
        ])
        
        return {"message": f"Mascota {mascota.codigo} actualizada correctamente."}
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
def delete_mascota(mascota_id: int):
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
async def upload_image(file: UploadFile = File(...)):
    try:
       
        res_cloudinary = subir_imagen(file.file, "mascotas")
        
        url = res_cloudinary["url"]
        codigo_cloudinary = res_cloudinary["public_id"] 

        
        conn = get_connection()
        cursor = conn.cursor()

       
        sql = """
            INSERT INTO imagenes_mascotas (codigo, link_imagen) 
            VALUES (:1, :2)
        """
        
        cursor.execute(sql, [codigo_cloudinary, url])
        conn.commit()

        return {
                "message": "Imagen guardada",
                "codigo_imagen": codigo_cloudinary,
                "url": url
                }

    except Exception as e:
        # ESTO es lo que nos dirá la verdad en el navegador
        print(f"ERROR REAL: {str(e)}") # Esto lo verás en la terminal
        raise HTTPException(status_code=500, detail=str(e)) # Esto lo verás en el F12
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()



