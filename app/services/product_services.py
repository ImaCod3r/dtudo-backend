from app.models.product import Product
from app.models.category import Category
from app.utils.generate_public_id import generate_public_id

def get_all_products():
    return list(Product.select())

def create_new_product(data):
    if 'category' not in data:
        return None, "Categoria é obrigatória."

    category_name = data.get('category')
    category = Category.select().where(Category.name == category_name).first()
    
    if not category:
        return None, "Categoria não encontrada."
    
    data['category'] = category
    data['public_id'] = generate_public_id('product')
    
    product = Product.create(**data)
    return product, None

def get_product_by_public_id(public_id):
    product = Product.get_or_none(Product.public_id == public_id)
    if not product:
        return None, "Produto não encontrado!"
    return product, None

def update_product_by_public_id(public_id, data):
    product = Product.get_or_none(Product.public_id == public_id)
    if not product:
        return None, "Produto não encontrado!"
    
    if 'category' in data:
        category_name = data['category']
        category = Category.select().where(Category.name == category_name).first()
        if not category:
            return None, "Categoria não encontrada."
        product.category = category
        del data['category']  # Remove category from data to avoid double assignment in loop

    for key, value in data.items():
        if hasattr(product, key):
            setattr(product, key, value)
    
    product.save()
    return product, None

def delete_product_by_public_id(public_id):
    product = Product.get_or_none(Product.public_id == public_id)
    if not product:
        return None, "Produto não encontrado!"
    
    product.delete_instance()
    return True, None