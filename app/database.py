from peewee import SqliteDatabase, Model

db = SqliteDatabase("dtudo.db")

class BaseModel(Model):
    class Meta:
        database = db