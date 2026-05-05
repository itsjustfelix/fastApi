import oracledb 
import os
from dotenv import load_dotenv

load_dotenv()

pool = oracledb.create_pool(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host="localhost",
    port=1521,
    service_name="xepdb1",
    min=1,
    max=5,
    increment=1
)

def get_connection():
    return pool.acquire()