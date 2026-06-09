from email_validator import validate_email, EmailNotValidError
from pydantic import BaseModel, field_validator, EmailStr
import re

class Propietarios_create(BaseModel):

    cedula : str
    nombreCompleto : str
    telefono : str
    sexo : str
    email : EmailStr
    contraseña : str
    rol : str = "3" # Asignamos el rol de administrador por defecto - Nunca cambiar este valor!!!! cambiar solamente si se cambia en la base de datos

    @field_validator('cedula')
    @classmethod
    def validate_cedula(cls, value):
        if not value:
            raise ValueError('La cédula es obligatoria')
        if len(value) < 6 or len(value) > 10:
            raise ValueError('La cédula debe tener entre 6 y 10 dígitos')
        if not value.isdigit():
            raise ValueError('La cédula debe contener solo números')
        return value
    
    @field_validator('nombreCompleto')
    @classmethod
    def validate_nombre_completo(cls, value):
        if not value:
            raise ValueError('El nombre es obligatorio')
        if len(value) < 3 or len(value) > 70:
            raise ValueError('El nombre completo debe tener entre 3 y 70 caracteres')
        if not all(char.isalpha() or char.isspace() for char in value):
            raise ValueError('El nombre completo debe contener solo letras y espacios')
        return value
    
    @field_validator('telefono')
    @classmethod
    def validate_telefono(cls, value):
        if not value:
            raise ValueError('El teléfono es obligatorio')
        if len(value) != 10:
            raise ValueError('El teléfono debe tener 10 dígitos')
        if not value.isdigit():
            raise ValueError('El teléfono debe contener solo números')
        return value
    
    @field_validator('sexo')
    @classmethod
    def validate_sexo(cls, value):
        if not value:
            raise ValueError('El sexo es obligatorio')
        if value not in ['M', 'F']:
            raise ValueError('El sexo debe ser "M" o "F"')
        return value
    
    @field_validator('email')
    @classmethod
    def validate_correo(cls, value):
        if not value:
            raise ValueError('El correo es obligatorio')
        try:
            validate_email(value)
        except EmailNotValidError:
            raise ValueError("El correo electrónico no es válido")
        return value
    
    @field_validator('contraseña')
    @classmethod
    def validate_contraseña(cls, value):
        if not value:
            raise ValueError('La contraseña es obligatoria')
        if len(value) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        if not re.search(r'[A-Z]', value):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula')
        if not re.search(r'[a-z]', value):
            raise ValueError('La contraseña debe contener al menos una letra minúscula')
        if not re.search(r'[0-9]', value):
            raise ValueError('La contraseña debe contener al menos un número')
        return value

class Propietarios_show(BaseModel):

    cedula : str
    nombre_completo : str
    telefono : str
    sexo : str
    email: EmailStr

    class Config:
        from_attributes = True

class Propietarios_update(BaseModel):

    cedula : str
    nombreCompleto : str
    telefono : str
    sexo : str

    @field_validator('nombreCompleto')
    @classmethod
    def validate_nombre_completo(cls, value):
        if not value:
            raise ValueError('El nombre es obligatorio')
        if len(value) < 3 or len(value) > 70:
            raise ValueError('El nombre completo debe tener entre 3 y 70 caracteres')
        if not all(char.isalpha() or char.isspace() for char in value):
            raise ValueError('El nombre completo debe contener solo letras y espacios')
        return value
    
    @field_validator('telefono')
    @classmethod
    def validate_telefono(cls, value):
        if not value:
            raise ValueError('El teléfono es obligatorio')
        if len(value) != 10:
            raise ValueError('El teléfono debe tener 10 dígitos')
        if not value.isdigit():
            raise ValueError('El teléfono debe contener solo números')
        return value
    
    @field_validator('sexo')
    @classmethod
    def validate_sexo(cls, value):
        if not value:
            raise ValueError('El sexo es obligatorio')
        if value not in ['M', 'F']:
            raise ValueError('El sexo debe ser "M" o "F"')
        return value
