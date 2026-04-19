from fastapi import APIRouter
from models.administradores import Administradores_create, Administradores_show, Administradores_update
from database.conexion import get_connection
router = APIRouter(
    prefix="/administradores",
    tags=["administradores"]
)

@router.get("")
def get_administradores():
    
    return {"message": "Lista de administradores"} 

@router.post("")
def create_administrador(admin: Administradores_create):
    return {"message": f"Administrador creado. Datos recibidos: {admin.cedula}, {admin.nombreCompleto}, {admin.telefono}, {admin.sexo}, {admin.email}"} 

@router.get("/{administrador_id}")
def get_administrador(administrador_id: int):
    return {"message": f"Detalles del administrador con ID {administrador_id}"}

@router.put("/{administrador_id}")
def update_administrador(administrador: Administradores_update):
    return {"message": f"Administrador con ID {administrador.cedula} actualizado"}

@router.delete("/{administrador_id}")
def delete_administrador(administrador_id: int):
    return {"message": f"Administrador con ID {administrador_id} eliminado"}
