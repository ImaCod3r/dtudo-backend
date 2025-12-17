from flask import Blueprint, jsonify, request
from app.services.category_services import get_all_categories, create_new_category, update_existing_category, delete_existing_category

categories_bp = Blueprint('categories', __name__)

@categories_bp.get('/')
def get_categories():
    categories = get_all_categories()
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
    

    if 'slug' not in data:
         return jsonify({
            'error': True,
            'message': 'Slug da categoria é obrigatório.'
        }), 400

    slug = data['name'].lower().replace(' ', '-')
    
    category, error = create_new_category(data['name'], slug)

    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 400

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

    category, error = update_existing_category(category_id, data['name'])

    if error:
        status = 404 if error == "Categoria não encontrada." else 400
        return jsonify({
            'error': True,
            'message': error
        }), status
        
    return jsonify({
        'error': False,
        'message': 'Categoria atualizada com sucesso!',
        'category': category.to_dict()
    }), 200
    
@categories_bp.delete('/<int:category_id>/delete')
def delete_category(category_id):
    success, error = delete_existing_category(category_id)
    
    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 404
        
    return jsonify({
        'error': False,
        'message': 'Categoria deletada com sucesso!'
    }), 200