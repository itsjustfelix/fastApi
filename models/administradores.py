from pydantic import BaseModel

class Administradores_create(BaseModel):
    cedula: str
    nombreCompleto: str
    telefono: str
    email: str
    contraseña: str
    rol : str = "1"

class Administradores_show(BaseModel):
    cedula: str
    nombre_completo: str
    telefono: str
    email: str
    class Config:
        from_attributes = True

class Administradores_update(BaseModel):
    cedula: str
    nombreCompleto: str
    telefono: str
    email: str
