from pydantic import BaseModel

class Veterinarios_create(BaseModel):
    cedula: str
    nombreCompleto: str
    telefono: str
    sexo: str
    codigo_especialidad: str
    email: str
    contraseña: str

class Veterinarios_show(BaseModel):
    cedula: str
    nombreCompleto: str
    telefono: str
    sexo: str
    especialidad: str
    email: str

    class Config:
        from_attributes = True


class Veterinarios_update(BaseModel):
    cedula: str
    nombreCompleto: str
    telefono: str
    sexo: str
    especialidad: str
    email: str
    contraseña: str