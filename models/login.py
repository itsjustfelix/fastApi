from pydantic import BaseModel, field_validator,EmailStr
from email_validator import validate_email, EmailNotValidError

class Login(BaseModel):
    email: EmailStr
    contraseña: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
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
        return value
