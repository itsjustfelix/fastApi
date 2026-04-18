from fastapi import APIRouter
from models.razas import Razas_create, Razas_show, Razas_update
from database.conexion import get_connection
router = APIRouter(
    prefix="/razas",
    tags=["razas"]
)

@router.get("")
def get_razas():
    return {"message": "Lista de razas"}

@router.post("")
def create_raza(raza: Razas_create):
    return {"message": f"Raza creada. Datos recibidos: {raza.codigo}, {raza.nombre}, {raza.codigo_especie}"}

@router.get("/{raza_id}")
def get_raza(raza_id: int):
    return {"message": f"Detalles de la raza con ID {raza_id}"}

@router.put("")
def update_raza(raza: Razas_update):
    return {"message": f"Raza con ID {raza.codigo} actualizada"}

@router.delete("/{raza_id}")
def delete_raza(raza_id: int):
    return {"message": f"Raza con ID {raza_id} eliminada"}

