from pydantic import BaseModel

class Propietarios_create(BaseModel):

    cedula : str
    nombreCompleto : str
    telefono : str
    sexo : str
    correo : str
    contraseña : str

class Propietarios_show(BaseModel):

    cedula : str
    nombreCompleto : str
    telefono : str
    sexo : str

    class Config:
        from_attributes = True

class Propietarios_update(BaseModel):

    cedula : str
    nombreCompleto : str
    telefono : str
    sexo : str
