from app.models.product import Product
from app.models.category import Category

def get_all_products():
    return list(Product.select())

def get_product_by_public_id(public_id):
    product = Product.get_or_none(Product.public_id == public_id)
    if not product:
        return None, "Produto não encontrado!"
    return product, None

def get_product_by_id(id):
    product = Product.get_or_none(Product.id == id)
    if not product:
        return None, "Produto não encontrado!"
    return product, None

def update(id, data):
    product = Product.get_or_none(Product.id == id)
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
        if key in ['image', 'category']:
            continue
        if hasattr(product, key):
            setattr(product, key, value)
    
    product.save()
    return product, None

def get_products_by_category_id(category_id):
    category = Category.get_or_none(Category.id == category_id)
    if not category:
        return None, "Categoria não encontrada."

    def collect_ids(cat):
        ids = [cat.id]
       
        for child in cat.children:
            ids.extend(collect_ids(child))
        return ids

    category_ids = collect_ids(category)
    products = list(Product.select().where(Product.category.in_(category_ids)))
    return products, None