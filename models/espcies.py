from pydantic import BaseModel

class especies_create(BaseModel):
    nombre: str

class especies_show(BaseModel):
    codigo: str
    nombre: str

    class Config:
        from_attributes = True
    
class especies_update(BaseModel):
    codigo: int
    nombre: str
