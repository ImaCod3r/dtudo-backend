from app.database import db
from app.models.user import User
from app.models.category import Category
from app.models.product import Product

def config_database():
    db.connect()
    db.create_tables([User, Category, Product])

    return db