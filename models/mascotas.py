from pydantic import BaseModel
from typing import Optional

class Masotas_create(BaseModel):
    nombre: str
    codigo_especie: str
    codigo_raza: str
    codigo_propietario: str
    codigo_imagen: Optional[str] = None


class Mascotas_show(BaseModel):
    codigo: int
    nombre: str
    nombre_especie: str
    nombre_raza: str
    link_imagen: str

    class Config:
        from_attributes = True

class Mascotas_update(BaseModel):
    codigo: int
    nombre: str
    codigo_especie: str
    codigo_raza: str

