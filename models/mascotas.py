from pydantic import BaseModel
from typing import Optional

class Masotas_create(BaseModel):
    nombre: str
    codigo_especie: str
    codigo_raza: str
    codigo_propietario: str
    link_imagen: Optional[str] = None


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

