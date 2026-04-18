from pydantic import BaseModel

class Especializaciones_create(BaseModel):
    nombre: str

class Especializaciones_show(BaseModel):
    codigo: str
    nombre: str

    class Config:
        from_attributes = True

class Especializaciones_update(BaseModel):
    codigo: int
    nombre: str