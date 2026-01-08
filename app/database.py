from peewee import MySQLDatabase, Model
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do MySQL a partir de variáveis de ambiente
db = MySQLDatabase(
    os.getenv("DB_NAME", "dtudo"),
    stale_timeout=300,
    max_connections=8,
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 3306)),
    charset='utf8mb4',
    thread_safe=True,
    autorollback=True,
    connect_timeout=10
)

class BaseModel(Model):
    class Meta:
        database = db