from pydantic import BaseModel

class Razas_create(BaseModel):
    nombre: str
    codigo_especie: str

class Razas_show(BaseModel):
    codigo: int
    nombre: str
    especie: str

    class Config:
        from_attributes = True

class Razas_update(BaseModel):
    codigo: int
    nombre: str
    codigo_especie: str