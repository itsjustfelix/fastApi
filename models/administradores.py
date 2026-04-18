from pydantic import BaseModel

class Administradores_create(BaseModel):
    cedula: str
    nombreCompleto: str
    telefono: str
    email: str
    contraseña: str

class Administradores_show(BaseModel):
    cedula: str
    nombreCompleto: str
    telefono: str
    email: str

    class Config:
        from_attributes = True

class Administradores_update(BaseModel):
    cedula: str
    nombreCompleto: str
    telefono: str
    email: str