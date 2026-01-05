from flask import Blueprint, request, jsonify
from app.services.user_services import get_all, update_role
from app.middlewares.auth_middlewares import auth_required

users_bp = Blueprint('users', __name__)

@users_bp.get('/')
def get_all_users():
    users = get_all()
    
    if not users:
        return jsonify({
            'error': True,
            'message': 'Nenhum usuário encontrado.'
        }), 404
        
    return jsonify({
        'error': True,
        'message': 'Usuários listados com sucesso!',
        'users': [user.to_dict() for user in users]
    }), 200
    
@users_bp.put("/user/<int:id>/role")
def update_user_role(id):
    data = request.get_json()
    user_id = id
    role = data.get("role")
    
    if not role:
        return jsonify({
            'error': True,
            'message': 'Informe o cargo.'
        }), 400
    try:
        role = update_role(user_id, role)
    except ValueError as error:
        if error != "Cargo inválido.":
            return jsonify({
                'error': True,
                'message': error
            }), 404
            
        return jsonify({
            'error': True,
            'message': error
        }), 400
    except Exception as e:
        print(e) 
        return jsonify({
            'error': True,
            'message': 'Erro ao atualizar o cargo.'
        }), 500
        
    return jsonify({
        'error': False,
        'message': f'Cargo atualizado para {role} com sucesso!'
    }), 201