from peewee import IntegrityError
from app.models.product import Product
from app.models.category import Category
from app.models.image import Image
from app.services.upload_services import save_image, delete_image_file

import math

def get_all_products(page=1, per_page=12):
    query = Product.select()
    total_count = query.count()
    products = list(query.paginate(page, per_page))
    return products, total_count


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

def create(data, image_file=None):
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    category_name = data.get("category")

    if not name or not price or not category_name:
        return None, "Tenha a certeza de que preencheu os campos obrigatórios."

    category = Category.select().where(Category.name == category_name).first()
    if not category:
        return None, "Categoria não encontrada!"

    image = None
    if image_file:
        try:
            image = save_image(image_file)
        except ValueError as e:
            return None, str(e)

    try:
        product = Product.create(
            name=name,
            description=description,
            category=category,
            price=price,
            image=image
        )
        return product, None
    except IntegrityError as e:
        if image:
            delete_image_file(image)
        return None, f"Erro de integridade ao salvar o produto: {str(e)}"
    except Exception as e:
        if image:
            delete_image_file(image)
        return None, f"Erro inesperado: {str(e)}"

def update(id, data, image_file=None):
    product = Product.get_or_none(Product.id == id)
    if not product:
        return None, "Produto não encontrado!"
    
    # Handle Image Update
    if image_file:
        try:
            # First save the new image
            new_image = save_image(image_file)
            
            # If successful, try to get and delete the old image
            old_image = None
            try:
                old_image = product.image
            except (Image.DoesNotExist, AttributeError):
                pass
            
            # Update product with new image
            product.image = new_image
            
            # Delete old image record and file if it existed
            if old_image:
                try:
                    delete_image_file(old_image)
                except Exception:
                    pass # Don't fail the whole update if old image deletion fails
        except ValueError as e:
            return None, str(e)

    # Handle Category Update
    if 'category' in data and data['category']:
        category_name = data['category']
        category = Category.get_or_none(Category.name == category_name)
        if not category:
            return None, "Categoria não encontrada."
        product.category = category

    # Update other fields
    allowed_fields = ['name', 'description', 'price']
    for key in allowed_fields:
        if key in data:
            setattr(product, key, data[key])
    
    try:
        product.save()
        return product, None
    except Exception as e:
        return None, f"Erro ao atualizar produto: {str(e)}"

def delete(id):
    product = Product.get_or_none(Product.id == id)
    if not product:
        return False, "Produto não encontrado!"
    
    try:
        if product.image:
            delete_image_file(product.image)
    except Image.DoesNotExist:
        pass
    except Exception:
        pass
    
    product.delete_instance()
    return True, None

def get_products_by_category_id(category_id, page=1, per_page=12):
    category = Category.get_or_none(Category.id == category_id)
    if not category:
        return None, 0, "Categoria não encontrada."

    def collect_ids(cat):
        ids = [cat.id]
        for child in cat.children:
            ids.extend(collect_ids(child))
        return ids

    category_ids = collect_ids(category)
    query = Product.select().where(Product.category.in_(category_ids))
    total_count = query.count()
    products = list(query.paginate(page, per_page))
    
    return products, total_count, None

def get_new_arrivals(page=1, per_page=12):
    query = Product.select().order_by(Product.created_at.desc())
    total_count = query.count()
    products = list(query.paginate(page, per_page))
    return products, total_count

def get_best_sellers(page=1, per_page=12):
    from app.models.orderItem import OrderItem
    from peewee import fn
    
    query = (Product
             .select(Product, fn.SUM(OrderItem.quantity).alias('total_sales'))
             .join(OrderItem, on=(Product.id == OrderItem.product))
             .group_by(Product)
             .order_by(fn.SUM(OrderItem.quantity).desc()))
    
    total_count = query.count()
    products = list(query.paginate(page, per_page))
    return products, total_count