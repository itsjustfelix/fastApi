from fastapi import APIRouter
from models.propietarios import Propietarios_create, Propietarios_show, Propietarios_update
from database.conexion import get_connection
router = APIRouter(
    prefix="/propietarios",
    tags=["propietarios"]
)

@router.get("")
def get_propietarios():
    return {"message": "Lista de propietarios"}


@router.post("")
def create_propietario(prop: Propietarios_create):
    return {"message": f"Propietario creado. Datos recibidos: {prop.cedula}, {prop.nombreCompleto}, {prop.telefono}, {prop.sexo}, {prop.email}"}

@router.get("/{propietario_id}")
def get_propietario(propietario_id: int):
    return {"message": f"Detalles del propietario con ID {propietario_id}"} 

@router.put("/{propietario_id}")
def update_propietario(propietario: Propietarios_update):
    return {"message": f"Propietario con ID {propietario.cedula} actualizado"} 

@router.delete("/{propietario_id}")
def delete_propietario(propietario_id: int):
    return {"message": f"Propietario con ID {propietario_id} eliminado"}    

