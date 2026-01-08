from playhouse.pool import PooledMySQLDatabase
from peewee import Model
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do MySQL com Pool para evitar estourar limite de conexões na Hostinger
db = PooledMySQLDatabase(
    os.getenv("DB_NAME", "dtudo"),
    max_connections=8,    # Limite conservador para planos compartilhados
    stale_timeout=300,    # Fecha conexões ociosas após 5 minutos
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 3306)),
    charset='utf8mb4'
)

class BaseModel(Model):
    class Meta:
        database = db