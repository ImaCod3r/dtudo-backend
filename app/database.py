from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin
from peewee import Model
import os
from dotenv import load_dotenv

load_dotenv()

max_connections = int(os.getenv("DB_MAX_CONNECTIONS", 500))
stale_timeout = int(os.getenv("DB_STALE_TIMEOUT", 300))
connect_timeout = int(os.getenv("DB_CONNECT_TIMEOUT", 10))
use_ssl = os.getenv("DB_USE_SSL", "false").lower() == "true"
ssl_params = {}


class ReconnectPooledMySQLDatabase(ReconnectMixin, PooledMySQLDatabase):
    pass


if use_ssl:
    ssl_ca = os.getenv("DB_SSL_CA")
    if ssl_ca:
        ssl_params = {"ssl": {"ca": ssl_ca}}

db = ReconnectPooledMySQLDatabase(
    os.getenv("DB_NAME", "dtudo"),
    max_connections=max_connections,
    stale_timeout=stale_timeout,
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 3306)),
    charset="utf8mb4",
    connect_timeout=connect_timeout,
    **ssl_params
)


class BaseModel(Model):
    class Meta:
        database = db
