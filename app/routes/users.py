from flask import Blueprint, request, jsonify
from app.services.user_services import get_all, update_role, update_profile

from app.middlewares.auth_middlewares import auth_required, is_admin

users_bp = Blueprint('users', __name__)

@users_bp.get('/')
@auth_required
@is_admin
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
@auth_required
@is_admin
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

@users_bp.put('/profile/update')
@auth_required
def update_user_profile():
    user_id = request.user_id
    
    # Suporta JSON ou Form Data (para arquivos)
    if request.is_json:
        data = request.get_json()
        image_file = None
    else:
        data = request.form.to_dict()
        image_file = request.files.get("avatar")
    
    user, error = update_profile(user_id, data, image_file)
    
    if error:
        return jsonify({
            'error': True,
            'message': error
        }), 400
        
    return jsonify({
        'error': False,
        'message': 'Perfil atualizado com sucesso!',
        'user': user.to_dict()
    }), 200