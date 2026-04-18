from fastapi import APIRouter
from models.consultas import Consultas_create, Consultas_show, Consultas_update
from database.conexion import get_connection
router = APIRouter(
    prefix="/consultas",
    tags=["consultas"]
)

@router.get("")
def get_consultas():
    return {"message": "Lista de consultas"}

@router.post("")
def create_consulta(consulta: Consultas_create):
    return {"message": f"Consulta creada. Datos recibidos: {consulta.fecha}, {consulta.hora}, {consulta.diadnostico}, {consulta.tratamiento}, {consulta.codigo_Mascotas}, {consulta.cedula_Veterinario}"}

@router.get("/{consulta_id}")
def get_consulta(consulta_id: int):
    return {"message": f"Detalles de la consulta con ID {consulta_id}"}

@router.put("")
def update_consulta(consulta: Consultas_update):
    return {"message": f"Consulta con ID {consulta.id} actualizada"}

@router.delete("/{consulta_id}")
def delete_consulta(consulta_id: int):
    return {"message": f"Consulta con ID {consulta_id} eliminada"}


