import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

def subir_imagen(archivo, carpeta: str) -> str:
    resultado = cloudinary.uploader.upload(
        archivo, 
        folder=carpeta
        )
    return {
        "url": resultado["secure_url"],
        "public_id": resultado["public_id"] 
    }


def eliminar_imagen(public_id: str):
    cloudinary.uploader.destroy(public_id)