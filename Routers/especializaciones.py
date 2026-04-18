from fastapi import APIRouter
from models.especializaciones import Especializaciones_create, Especializaciones_show, Especializaciones_update
from database.conexion import get_connection
router = APIRouter(
    prefix="/especializaciones",
    tags=["especializaciones"]
)


@router.get("")
def get_especializaciones():
    return {"message": "Lista de especializaciones"}

@router.post("")
def create_especializacion(especializacion: Especializaciones_create):
    return {"message": f"Especialización creada. Datos recibidos: {especializacion.codigo}, {especializacion.nombre}"}

@router.get("/{especializacion_id}")
def get_especializacion(especializacion_id: int):
    return {"message": f"Detalles de la especialización con ID {especializacion_id}"}

@router.put("")
def update_especializacion(especializacion: Especializaciones_update):
    return {"message": f"Especialización con ID {especializacion.codigo} actualizada"}