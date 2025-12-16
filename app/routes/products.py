from flask import Blueprint, jsonify, request
from app.utils.generate_public_id import generate_public_id
from app.models.product import Product
from app.models.category import Category

products_bp = Blueprint('products', __name__)
    
@products_bp.get('/')
def get_products():
    products = Product.select()
    return jsonify({
        'error': False,
        'message': 'Produtos listados com sucesso!',
        'products': [product.to_dict() for product in products]
    })

@products_bp.post('/new')
def create_product():
    data = request.get_json()
    data['public_id'] = generate_public_id('product')
    if not 'category' in data:
        return jsonify({
            'error': True,
            'message': 'Categoria é obrigatória.'
        }), 400
    
    data['category'] = Category.select().where(Category.name == data.get('category')).first()
    
    if not data['category']:
        return jsonify({
            'error': True,
            'message': 'Categoria não encontrada.'
        }), 404

    product = Product.create(**data)

    return jsonify({
        'error': False,
        'message': 'Produto criado com sucesso!',
        'product': product.to_dict()
    }), 201

@products_bp.get('/<public_id>')
def get_product(public_id):
    product = Product.get_or_none(Product.public_id == public_id)
    if product:
        return jsonify({
            'error': False,
            'message': 'Produto encontrado com sucesso!',
            'product': product.to_dict()
        })
    return jsonify({
        'error': True,
        'message': 'Produto não encontrado!'
    }), 404

@products_bp.put('/<public_id>')
def update_product(public_id):
    data = request.get_json()
    product = Product.get_or_none(Product.public_id == public_id)
    if product:
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return jsonify({
            'error': False,
            'message': 'Produto atualizado com sucesso!',
            'product': product.to_dict()
        })
    return jsonify({
        'error': True,
        'message': 'Produto não encontrado!'
    }), 404

@products_bp.delete('/<public_id>')
def delete_product(public_id):
    product = Product.get_or_none(Product.public_id == public_id)
    if product:
        product.delete_instance()
        return jsonify({
            'error': False,
            'message': 'Produto deletado com sucesso!'
        })
    return jsonify({
        'error': True,
        'message': 'Produto não encontrado!'
    }), 404