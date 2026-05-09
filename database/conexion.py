import oracledb 
import os
from dotenv import load_dotenv

load_dotenv()

pool = oracledb.create_pool(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    service_name=os.getenv("DB_SERVICE_NAME"),
    min=1,
    max=5,
    increment=1
)

def get_connection():
    return pool.acquire()