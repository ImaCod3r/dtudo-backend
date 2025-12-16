from flask import Blueprint, jsonify, request
from app.models.category import Category

categories_bp = Blueprint('categories', __name__)

@categories_bp.get('/')
def get_categories():
    categories = Category.select()
    categories_list = [category.to_dict() for category in categories]
    return jsonify({
        'error': False,
        'message': 'Categorias listadas com sucesso!',
        'categories': categories_list
    }), 200

@categories_bp.post('/new')
def create_category():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({
            'error': True,
            'message': 'Nome da categoria é obrigatório.'
        }), 400
    
    if not data or 'slug' not in data:
        return jsonify({
            'error': True,
            'message': 'Slug da categoria é obrigatório.'
        }), 400

    if Category.select().where(Category.name == data['name']).exists():
        return jsonify({
            'error': True,
            'message': 'Categoria já existe.'
        }), 400

    category = Category.create(name=data['name'], slug=data['name'].lower().replace(' ', '-'))
    return jsonify({
        'error': False,
        'message': 'Categoria criada com sucesso!',
        'category': category.to_dict()
    }), 201

@categories_bp.put('/<int:category_id>/edit')
def edit_category(category_id):
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({
            'error': True,
            'message': 'Nome da categoria é obrigatório.'
        }), 400

    try:
        category = Category.get_by_id(category_id)
        category.name = data['name']
        category.save()
        return jsonify({
            'error': False,
            'message': 'Categoria atualizada com sucesso!',
            'category': category.to_dict()
        }), 200
    except Category.DoesNotExist:
        return jsonify({
            'error': True,
            'message': 'Categoria não encontrada.'
        }), 404
    
@categories_bp.delete('/<int:category_id>/delete')
def delete_category(category_id):
    try:
        category = Category.get_by_id(category_id)
        category.delete_instance()
        return jsonify({
            'error': False,
            'message': 'Categoria deletada com sucesso!'
        }), 200
    except Category.DoesNotExist:
        return jsonify({
            'error': True,
            'message': 'Categoria não encontrada.'
        }), 404