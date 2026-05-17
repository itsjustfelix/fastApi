from pydantic import BaseModel, field_validator
from typing import Optional

class Mascotas_create(BaseModel):
    nombre: str
    codigo_especie: str
    codigo_raza: str
    codigo_propietario: str
    link_imagen: Optional[str] = None

    @field_validator('nombre')
    @classmethod
    def validate_nombre(cls, value):    
        if not value:
            raise ValueError('El nombre es obligatorio')
        if len(value) < 3 or len(value) > 20:
            raise ValueError('El nombre debe tener entre 3 y 20 caracteres')
        if not all(char.isalpha() or char.isspace() for char in value):
            raise ValueError('El nombre debe contener solo letras y espacios')
        return value

class Mascotas_show(BaseModel):
    codigo: int
    nombre: str
    codigo_especie: str
    nombre_especie: str
    codigo_raza: str
    nombre_raza: str
    link_imagen: Optional[str] = None

    class Config:
        from_attributes = True

class Mascotas_update(BaseModel):
    nombre: str
    codigo_especie: str
    codigo_raza: str

    @field_validator('nombre')
    @classmethod
    def validate_nombre(cls, value):
        if not value:
            raise ValueError('El nombre es obligatorio')
        if len(value) < 3 or len(value) > 20:
            raise ValueError('El nombre debe tener entre 3 y 20 caracteres')
        if not all(char.isalpha() or char.isspace() for char in value):
            raise ValueError('El nombre debe contener solo letras y espacios')
        return value
