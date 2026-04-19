from pydantic import BaseModel

class Masotas_create(BaseModel):
    nombre: str
    codigo_especie: str
    codigo_raza: str
    cedula_propietario: str
    link_imagen: str


class Mascotas_show(BaseModel):
    codigo: int
    nombre: str
    especie: str
    raza: str
    propietario: str
    link_imagen: str

    class Config:
        from_attributes = True

class Mascotas_update(BaseModel):
    codigo: int
    nombre: str
    codigo_especie: str
    codigo_raza: str

