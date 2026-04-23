from pydantic import BaseModel

class Propietarios_create(BaseModel):

    cedula : str
    nombreCompleto : str
    telefono : str
    sexo : str
    email : str
    contraseña : str
    rol : str = "3"

class Propietarios_show(BaseModel):

    cedula : str
    nombre_completo : str
    telefono : str
    sexo : str
    email: str

    class Config:
        from_attributes = True

class Propietarios_update(BaseModel):

    cedula : str
    nombreCompleto : str
    telefono : str
    sexo : str
