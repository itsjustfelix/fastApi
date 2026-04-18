from pydantic import BaseModel

class Consultas_create(BaseModel):
    fecha: str
    hora: str
    diadnostico: str
    tratamiento: str
    codigo_Mascotas: str
    cedula_Veterinario: str


class Consultas_show(BaseModel):
    id: str
    fecha: str
    hora: str
    diadnostico: str
    tratamiento: str
    masocta: str
    veterinario: str

    class Config:
        from_attributes = True

class Consultas_update(BaseModel):
    id: str
    diadnostico: str
    tratamiento: str
    codigo_Mascota: str
    cedula_Veterinario: str