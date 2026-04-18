from fastapi import APIRouter
from models.veterinarios import Veterinarios_create, Veterinarios_show, Veterinarios_update
from database.conexion import get_connection
router = APIRouter(
    prefix="/veterinarios",
    tags=["veterinarios"]
)

@router.get("")
def get_veterinarios():
    return {"message": "Lista de veterinarios"}

@router.post("")
def create_veterinario(veterinario: Veterinarios_create):
    return {"message": f"Veterinario creado. Datos recibidos: {veterinario.cedula}, {veterinario.nombreCompleto}, {veterinario.telefono}, {veterinario.sexo}, {veterinario.codigo_especialidad}, {veterinario.email}"}

@router.get("/{veterinario_id}")
def get_veterinario(veterinario_id: int):
    return {"message": f"Detalles del veterinario con ID {veterinario_id}"}

@router.put("")
def update_veterinario(veterinario: Veterinarios_update):
    return {"message": f"Veterinario con ID {veterinario.cedula} actualizado"}

@router.delete("/{veterinario_id}")
def delete_veterinario(veterinario_id: int):
    return {"message": f"Veterinario con ID {veterinario_id} eliminado"}

