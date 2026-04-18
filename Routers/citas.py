from fastapi import APIRouter
from models.citas import Citas_create, Citas_show, Citas_update
from database.conexion import get_connection
router = APIRouter(
    prefix="/citas",
    tags=["citas"]
)

@router.get("")
def get_citas():
    return {"message": "Lista de citas"}

@router.post("")
def create_cita(cita: Citas_create):
    return {"message": f"Cita creada. Datos recibidos: {cita.fecha}, {cita.hora}, {cita.motivo}, {cita.cedula_veterinario}, {cita.cedula_cliente}"}

@router.get("/{cita_id}")
def get_cita(cita_id: int):
    return {"message": f"Detalles de la cita con ID {cita_id}"}

@router.put("")
def update_cita(cita: Citas_update):
    return {"message": f"Cita con ID {cita.id} actualizada"}

@router.delete("/{cita_id}")
def delete_cita(cita_id: int):   
    return {"message": f"Cita con ID {cita_id} eliminada"}      

