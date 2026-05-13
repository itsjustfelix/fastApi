from pydantic import BaseModel

class Veterinarios_create(BaseModel):
    cedula: str
    nombreCompleto: str
    telefono: str
    sexo: str
    codigo_especialidad: str
    email: str
    contraseña: str
    rol: str = "2"

class Veterinarios_show(BaseModel):
    cedula: str
    nombre_completo: str
    sexo: str
    telefono: str
    nombre_especializacion: str

    class Config:
        from_attributes = True


class Veterinarios_update(BaseModel):
    cedula: str
    nombreCompleto: str
    telefono: str
    sexo: str
    codigo_especialidad: str