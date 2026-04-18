from fastapi import APIRouter
from models.mascotas import Masotas_create, Mascotas_show, Mascotas_update
from database.conexion import get_connection
router = APIRouter(
    prefix="/mascotas",
    tags=["mascotas"]
)

@router.get("")
def get_mascotas():
    return {"message": "Lista de mascotas"} 

@router.post("")
def create_mascota(mascota: Masotas_create):
    return {"message": f"Mascota creada. Datos recibidos: {mascota.codigo}, {mascota.nombre}, {mascota.edad}, {mascota.sexo}, {mascota.peso}, {mascota.codigo_Especie}"}

@router.get("/{mascota_id}")
def get_mascota(mascota_id: int):   
    return {"message": f"Detalles de la mascota con ID {mascota_id}"}   


@router.put("")
def update_mascota(mascota: Mascotas_update):
    return {"message": f"Mascota con ID {mascota.codigo} actualizada"}

@router.delete("/{mascota_id}")
def delete_mascota(mascota_id: int):
    return {"message": f"Mascota con ID {mascota_id} eliminada"}

