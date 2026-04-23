from pydantic import BaseModel

class Consultas_create(BaseModel):
    fecha: str
    descripcion: str
    diagnostico: str
    tratamiento: str
    codigo_Mascotas: str
    cedula_Veterinario: str
    codigo_cita : str
    codigo_especializacion: str


class Consultas_show(BaseModel):
    codigo: str
    fecha: str
    descripcion :str
    diagnostico: str
    tratamiento: str
    nombre_mascota: str
    nombre_veterinario: str
    nombre_especializacion: str

    class Config:
        from_attributes = True

class Consultas_update(BaseModel):
    id: str
    descripcion: str
    diagnostico: str
    tratamiento: str