import cloudinary
import cloudinary.uploader
import os
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

def subir_imagen(archivo, carpeta: str) -> str:
    try:
        resultado = cloudinary.uploader.upload(
            archivo, 
            folder=carpeta
            )
        return {
            "url": resultado["secure_url"],
        }
    except Exception as e:
        print(f"ERROR CLOUDINARY: {str(e)}")  # ← verás esto en la terminal de FastAPI
        raise HTTPException(status_code=500, detail=str(e))

def eliminar_imagen(public_id: str):
    cloudinary.uploader.destroy(public_id)