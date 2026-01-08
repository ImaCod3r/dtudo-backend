from peewee import MySQLDatabase, Model
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do MySQL a partir de variáveis de ambiente
db = MySQLDatabase(
    os.getenv("DB_NAME", "dtudo"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 3306)),
    charset='utf8mb4'
)

class BaseModel(Model):
    class Meta:
        database = db