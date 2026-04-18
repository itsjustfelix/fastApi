from fastapi import APIRouter
from models.espcies import especies_create, especies_show, especies_update
from database.conexion import get_connection
router = APIRouter(
    prefix="/especies",
    tags=["especies"]
)

@router.get("")
def get_especies():
    return {"message": "Lista de especies"}


@router.post("")
def create_especie(especie: especies_create):
    return {"message": f"Especie creada. Datos recibidos: {especie.codigo}, {especie.nombre}"}

@router.get("/{especie_id}")
def get_especie(especie_id: int):
    return {"message": f"Detalles de la especie con ID {especie_id}"}


@router.put("")
def update_especie(especie: especies_update):
    return {"message": f"Especie con ID {especie.codigo} actualizada"}


@router.delete("/{especie_id}")
def delete_especie(especie_id: int):
    return {"message": f"Especie con ID {especie_id} eliminada"}

