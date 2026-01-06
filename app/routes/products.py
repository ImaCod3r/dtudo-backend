from flask import Blueprint, jsonify, request
from peewee import IntegrityError
from app.services.product_services import (
    get_all_products, 
    get_product_by_id, 
    update, 
    create,
    delete,
    get_products_by_category_id, 
    get_product_by_public_id
)
from app.middlewares.auth_middlewares import auth_required, is_admin

products_bp = Blueprint('products', __name__)
    
@products_bp.get('/')
def get_products():
    try:
        products = get_all_products()
        return jsonify({
            'error': False,
            'message': 'Produtos listados com sucesso!',
            'products': [product.to_dict() for product in products]
        })
    except Exception as e:
        return jsonify({
            "error": True,
            "message": f"Erro interno: {str(e)}"
        }), 500

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
# @auth_required
# @is_admin
def create_product():
    data = request.form
    image_file = request.files.get("image")

    product, error = create(data, image_file)

    if error:
        return jsonify({
            "error": True,
            "message": error
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

@products_bp.put('/<int:id>/update')
# @auth_required
# @is_admin
def update_product(id):
    data = request.form
    image_file = request.files.get("image")
    
    product, error = update(id, data, image_file)
    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 400

    return jsonify({
        'error': False,
        'message': 'Produto atualizado com sucesso!',
        'Produto': product.to_dict()
    })

@products_bp.delete('/<int:id>')
# @auth_required
# @is_admin
def delete_product(id):
    success, error = delete(id)

    if not success:
        return jsonify({
            'error': True,
            'message': error or 'Não foi possível deletar o produto.'
        }), 400
    
    return jsonify({
        'error': False,
        'message': 'Produto deletado com sucesso!'
    }), 200