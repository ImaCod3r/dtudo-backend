from flask import Blueprint, jsonify, request, make_response
from peewee import IntegrityError
from app.models.product import Product
from app.models.category import Category
from app.services.product_services import get_all_products, get_product_by_public_id, update, delete_product_by_public_id, get_products_by_category_id
from app.services.upload_services import save_image, delete_image_file
from app.middlewares.auth_middlewares import auth_required, is_admin

products_bp = Blueprint('products', __name__)
    
@products_bp.get('/')
def get_products():
    try:
        products = get_all_products()
    except IntegrityError:
        return jsonify({
            "error": False,
            "message": "Não foi possível listar produtos"
        })
    
    return jsonify({
        'error': False,
        'message': 'Produtos listados com sucesso!',
        'products': [product.to_dict() for product in products]
    })

@products_bp.get('/category/<int:category_id>')
def get_products_by_category(category_id):
    products, error = get_products_by_category_id(category_id)
    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 404

    return jsonify({
        'error': False,
        'message': 'Produtos listados por categoria com sucesso!',
        'products': [product.to_dict() for product in products]
    })

@products_bp.post('/new')
@auth_required
@is_admin
def create_product():
    data = request.form
    image_file = request.files.get("image")

    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    category_name = data.get("category")

    try:
        image = save_image(image_file) if image_file else None
    except ValueError as e: 
        return jsonify({
            "error": True,
            "message": str(e)
        }), 400

    if not name or not price or not category_name:
        return jsonify({
            "error": True,
            "message": "Tenha a certeza de que preencheu os campos obrigatórios."
        }), 400
    
    category = Category.select().where(Category.name == category_name).first()

    if not category:
        return jsonify({
            "error": True,
            "message": "Categoria não encontrada!"
        }), 404
    
    try: 
        product = Product.create(
            name=name,
            description=description,
            category=category,
            price=price,
            image=image,
        )
    except IntegrityError:
        delete_image_file(image)
        return jsonify({
            "error": True,
            "message": "Não foi possível salvar o produto."
        }), 400
    return jsonify({
        "error": False,
        "message": "Produto cadastrado com sucesso!",
        "Produto": product.to_dict()
    }), 201
        
@products_bp.get('/<public_id>')
def get_product(public_id):
    product, error = get_product_by_public_id(public_id)
    
    if error:
         return jsonify({
            'error': True,
            'message': error
        }), 404
        
    return jsonify({
        'error': False,
        'message': 'Produto encontrado com sucesso!',
        'product': product.to_dict()
    })

@products_bp.put('/<int:id>')
@auth_required
@is_admin
def update_product(id):
    data = request.form
    
    product, error = update(id, data)

    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 404

    return jsonify({
        'error': False,
        'message': 'Produto atualizado com sucesso!',
        'product': product.to_dict()
    })

@products_bp.delete('/<public_id>')
@auth_required
@is_admin
def delete_product(public_id):
    product, error = get_product_by_public_id(public_id)

    if error:
        return jsonify({
            'error': True,
            'message': 'Produto não encontrado.'
        })

    if product.image:
        delete_image_file(product.image)

    success, _ = delete_product_by_public_id(public_id)

    if success:
        return jsonify({
            'error': False,
            'message': 'Produto deletado com sucesso!'
        })
    
    return jsonify({
        'error': True,
        'message': 'Não foi possível deletar o produto.'
    })