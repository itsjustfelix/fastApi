from pydantic import BaseModel

class Citas_create(BaseModel):
    fecha: str
    hora: str
    codigoMascota: str
    cedulaVeterinario: str

class Citas_show(BaseModel):
    codigo: int
    fecha: str
    hora: str
    mascota: str
    veterinario: str
    estado: str

    class Config:
        from_attributes = True

class Citas_update(BaseModel):
    codigo : int
    fecha: str
    hora: str


