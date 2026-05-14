from pydantic import BaseModel

class Citas_create(BaseModel):
    fecha: str
    hora: str
    codigoMascota: str
    codigoEspecializacion: str
    cedulaVeterinario: str

class Citas_show(BaseModel):
    codigo: str
    fecha: str
    hora: str
    nombre_mascota: str
    nombre_veterinario: str
    estado_cita: str
    nombre_especializacion: str

    class Config:
        from_attributes = True

class Citas_update(BaseModel):
    codigo : str
    fecha: str
    hora: str


