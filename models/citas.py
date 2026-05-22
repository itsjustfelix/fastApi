from pydantic import BaseModel, field_validator

class Citas_create(BaseModel):
    fecha: str
    hora: str
    codigoMascota: str
    codigoEspecializacion: str
    cedulaVeterinario: str

    @field_validator('fecha')
    @classmethod
    def validate_fecha(cls, value):
        if not value:
            raise ValueError('La fecha es obligatoria')
        return value

    @field_validator('hora')
    @classmethod
    def validate_hora(cls, value):
        if not value:
            raise ValueError('La hora es obligatoria')
        return value

    @field_validator('codigoMascota')
    @classmethod
    def validate_codigo_mascota(cls, value):
        if not value:
            raise ValueError('El código de la mascota es obligatorio')
        return value
    
    @field_validator('codigoEspecializacion')
    @classmethod
    def validate_codigo_especializacion(cls, value):
        if not value:
            raise ValueError('El código de la especialización es obligatorio')
        return value
    
    @field_validator('cedulaVeterinario')
    @classmethod
    def validate_cedula_veterinario(cls, value):
        if not value:
            raise ValueError('La cédula del veterinario es obligatoria')
        return value

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

class Citas_show_veterinario(BaseModel):
    codigo: str
    fecha: str
    hora: str
    nombre_mascota: str
    estado_cita: str
    
    class Config:
        from_attributes = True

class Citas_update(BaseModel):
    codigo : str
    fecha: str
    hora: str

    @field_validator('fecha')
    @classmethod
    def validate_fecha(cls, value):
        if not value:
            raise ValueError('La fecha es obligatoria')
        return value
    
    @field_validator('hora')
    @classmethod
    def validate_hora(cls, value):
        if not value:
            raise ValueError('La hora es obligatoria')
        return value


