from pydantic import BaseModel, field_validator

class Razas_create(BaseModel):
    nombre: str
    codigo_especie: str
    @field_validator('nombre')
    @classmethod
    def validate_nombre(cls, value):
        if not value:
            raise ValueError('El nombre es obligatorio')
        if len(value) < 3 or len(value) > 20:
            raise ValueError('El nombre debe tener entre 3 y 20 caracteres')
        if not all(char.isalpha() or char.isspace() for char in value):
            raise ValueError('El nombre debe contener solo letras y espacios')
        return value

class Razas_show(BaseModel):
    codigo: int
    nombre: str
    nombre_especie: str 

    class Config:
        from_attributes = True

class Razas_option(BaseModel):
    codigo: int
    nombre: str
    
    class Config:
        from_attributes = True

class Razas_update(BaseModel):
    codigo: int
    nombre: str
    codigo_especie: str

    @field_validator('nombre')
    @classmethod
    def validate_nombre(cls, value):
        if not value:
            raise ValueError('El nombre es obligatorio')
        if len(value) < 3 or len(value) > 20:
            raise ValueError('El nombre debe tener entre 3 y 20 caracteres')
        if not all(char.isalpha() or char.isspace() for char in value):
            raise ValueError('El nombre debe contener solo letras y espacios')
        return value