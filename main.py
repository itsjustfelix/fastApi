from fastapi import FastAPI
from Routers.administradores import router as administradores_router
from Routers.propietarios import router as propietarios_router
from Routers.citas import router as citas_router
from Routers.mascotas import router as mascotas_router
from Routers.especializaciones import router as especializaciones_router
from Routers.veterinarios import router as veterinarios_router
from Routers.razas import router as razas_router
from Routers.loggin import router as loggin_router
from Routers.cosnultas import router as consultas_router
from database.conexion import get_connection




app = FastAPI()


@app.get("/")
def menasa():
    return {"message": "Hello mundo!"}


@app.get("/usuarios")
def obtener_usuarios():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM roles")

        columnas = [col[0] for col in cursor.description]
        datos = []

        for fila in cursor:
            datos.append(dict(zip(columnas, fila)))

        cursor.close()
        conn.close()

        return datos

    except Exception as e:
        return {"error": str(e)}
    

app.include_router(administradores_router)
app.include_router(propietarios_router)
app.include_router(citas_router)
app.include_router(mascotas_router)
app.include_router(especializaciones_router)
app.include_router(veterinarios_router)
app.include_router(razas_router)
app.include_router(consultas_router)
app.include_router(loggin_router)

