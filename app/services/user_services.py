from app.models.user import User
from flask import request

def get_user_by_id(id):
    user = User.get_or_none(User.id == id)
    return user

def get_user_by_public_id(public_id):
    user = User.get_or_none(User.public_id == public_id)
    return user

def get_all():
    users = list(User.select())
    
    return users

def update_role(user_id, role):
    user = User.get_by_id(user_id)
    
    if not user:
        raise ValueError("Usuário não encontrado.")

    valid_roles = {"customer", "admin"}

    if role not in valid_roles:
        raise ValueError("Cargo inválido.")

    user.role = role
    user.save()
    
    return user.to_dict().get("role")
    
    