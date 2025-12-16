from flask import Blueprint, jsonify, request
from app.models import Product

products_bp = Blueprint('products', __name__)
    
@products_bp.get('/products')
def get_products():
    products = Product.select()
    return jsonify({
        'error': False,
        'message': 'Produtos listados com sucesso!',
        'products': [product.to_dict() for product in products]
    })

@products_bp.post('/products')
def create_product():
    data = request.get_json()
    product = Product.create(**data)
    return jsonify({
        'error': False,
        'message': 'Produto criado com sucesso!',
        'product': product.to_dict()
    }), 201

@products_bp.get('/products/<public_id>')
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

@products_bp.put('/products/<public_id>')
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

@products_bp.delete('/products/<public_id>')
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

def to_dict(self):
    return {
        'id': self.id,
        'name': self.name,
        'description': self.description,
        'price': self.price,
        'stock': self.stock,
        'image_url': self.image_url,
        'category_id': self.category.id if self.category else None,
        'public_id': self.public_id
    }