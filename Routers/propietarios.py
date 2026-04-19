from fastapi import APIRouter
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
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM propietarios")

        columnas = [col[0] for col in cursor.description]
        datos = []

        for fila in cursor:
            datos.append(dict(zip(columnas, fila)))

        cursor.close()
        conn.close()

        return datos

    except Exception as e:
        return {"error": str(e)}


@router.post("")
def create_propietario(prop: Propietarios_create):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        codigo_usuario = cursor.callfunc("PKG_USUARIO.FN_guardar_usuario", str,
                                         [prop.email, hashear_password(prop.contraseña), prop.rol])

        cursor.execute("INSERT INTO propietarios (CEDULA, NOMBRE_COMPLETO, TELEFONO, SEXO, CODIGO_USUARIO) VALUES (:1, :2, :3, :4, :5)",
                       (prop.cedula, prop.nombreCompleto, prop.telefono, prop.sexo, codigo_usuario))
        conn.commit()

        cursor.close()
        conn.close()

        return {"message": f"Propietario creado. Datos recibidos: {prop.cedula}, {prop.nombreCompleto}, {prop.telefono}, {prop.sexo}, {prop.email}"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/{propietario_id}")
def get_propietario(propietario_id: int):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM propietarios WHERE cedula = %s", (propietario_id,))
        fila = cursor.fetchone()

        if fila:
            columnas = [col[0] for col in cursor.description]
            propietario = dict(zip(columnas, fila))
        else:
            propietario = None

        cursor.close()
        conn.close()

        if propietario:
            return propietario
        else:
            return {"message": f"No se encontró un propietario con ID {propietario_id}"}    
    except Exception as e:
        return {"error": str(e)}

@router.put("/{propietario_id}")
def update_propietario(propietario: Propietarios_update):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE propietarios SET nombreCompleto = %s, telefono = %s, sexo = %s WHERE cedula = %s",
                       (propietario.nombreCompleto, propietario.telefono, propietario.sexo, propietario.cedula))
        conn.commit()

        cursor.close()
        conn.close()

        return {"message": f"Propietario con ID {propietario.cedula} actualizado"}
    except Exception as e:
        return {"error": str(e)}

@router.delete("/{propietario_id}")
def delete_propietario(propietario_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM propietarios WHERE cedula = %s", (propietario_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return {"message": f"Propietario con ID {propietario_id} eliminado"}
    except Exception as e:
        return {"error": str(e)}
