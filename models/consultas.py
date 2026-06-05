from pydantic import BaseModel, field_validator
from typing import Optional

class Consultas_create(BaseModel):
    fecha: str
    descripcion: str
    diagnostico: str
    tratamiento: str
    codigo_Mascotas: str
    cedula_Veterinario: str
    codigo_cita : str
    codigo_especializacion: str

    @field_validator('fecha')
    @classmethod
    def validate_fecha(cls, value):
        if not value:
            raise ValueError('La fecha es obligatoria')
        return value

    @field_validator('descripcion')
    @classmethod
    def validate_descripcion(cls, value):
        if not value:
            raise ValueError('La descripción es obligatoria')
        return value

    @field_validator('diagnostico')
    @classmethod
    def validate_diagnostico(cls, value):
        if not value:
            raise ValueError('El diagnóstico es obligatorio')
        return value

    @field_validator('tratamiento')
    @classmethod
    def validate_tratamiento(cls, value):
        if not value:
            raise ValueError('El tratamiento es obligatorio')
        return value

    @field_validator('codigo_Mascotas')
    @classmethod
    def validate_codigo_mascotas(cls, value):
        if not value:
            raise ValueError('El código de la mascota es obligatorio')
        return value

    @field_validator('cedula_Veterinario')
    @classmethod
    def validate_cedula_veterinario(cls, value):
        if not value:
            raise ValueError('La cédula del veterinario es obligatoria')
        return value

    @field_validator('codigo_cita')
    @classmethod
    def validate_codigo_cita(cls, value):
        if not value:
            raise ValueError('El código de la cita es obligatorio')
        return value

    @field_validator('codigo_especializacion')
    @classmethod
    def validate_codigo_especializacion(cls, value):
        if not value:
            raise ValueError('El código de la especialización es obligatorio')
        return value

class Consultas_show(BaseModel):
    codigo: str
    fecha: str
    descripcion :str
    diagnostico: str
    tratamiento: str
    codigo_mascota : Optional[str] = None
    nombre_mascota: str
    nombre_veterinario: str
    nombre_especializacion: str

    class Config:
        from_attributes = True

class Consultas_update(BaseModel):
    codigo: str
    descripcion: str
    diagnostico: str
    tratamiento: str
    @field_validator('descripcion')
    @classmethod
    def validate_descripcion(cls, value):
        if not value:
            raise ValueError('La descripción es obligatoria')
        return value
    
    @field_validator('diagnostico')
    @classmethod
    def validate_diagnostico(cls, value):
        if not value:
            raise ValueError('El diagnóstico es obligatorio')
        return value
    
    @field_validator('tratamiento')
    @classmethod
    def validate_tratamiento(cls, value):
        if not value:
            raise ValueError('El tratamiento es obligatorio')
        return value