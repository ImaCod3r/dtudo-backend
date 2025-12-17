from flask import Blueprint, jsonify, request
from app.services.product_services import get_all_products, create_new_product, get_product_by_public_id, update_product_by_public_id, delete_product_by_public_id

products_bp = Blueprint('products', __name__)
    
@products_bp.get('/')
def get_products():
    products = get_all_products()
    return jsonify({
        'error': False,
        'message': 'Produtos listados com sucesso!',
        'products': [product.to_dict() for product in products]
    })

@products_bp.post('/new')
def create_product():
    data = request.get_json()
    
    product, error = create_new_product(data)
    
    if error:
        # Determine error code based on message
        status = 404 if "não encontrada" in error else 400
        return jsonify({
            'error': True,
            'message': error
        }), status

    return jsonify({
        'error': False,
        'message': 'Produto criado com sucesso!',
        'product': product.to_dict()
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

@products_bp.put('/<public_id>')
def update_product(public_id):
    data = request.get_json()
    product, error = update_product_by_public_id(public_id, data)
    
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
def delete_product(public_id):
    success, error = delete_product_by_public_id(public_id)
    
    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 404
        
    return jsonify({
        'error': False,
        'message': 'Produto deletado com sucesso!'
    })