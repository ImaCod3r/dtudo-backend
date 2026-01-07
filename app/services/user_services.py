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
    user = User.get_or_none(User.id == user_id)
    
    if not user:
        raise ValueError("Usuário não encontrado.")

    valid_roles = {"customer", "admin"}

    if role not in valid_roles:
        raise ValueError("Cargo inválido.")

    user.role = role
    user.save()

def update_profile(user_id, data, image_file=None):
    user = User.get_or_none(User.id == user_id)
    
    if not user:
        return None, "Usuário não encontrado."

    name = data.get("name")
    phone = data.get("phone")

    if name:
        user.name = name
    
    if phone:
        from app.utils.validators import validate_angolan_phone, format_angolan_phone
        if not validate_angolan_phone(phone):
            return None, "Número de telefone angolano inválido."
        user.phone = format_angolan_phone(phone)
    
    if image_file:
        from app.services.upload_services import save_image
        try:
            image = save_image(image_file, folder="users")
            user.avatar = image.url
        except ValueError as e:
            return None, str(e)
    elif "avatar" in data:
        user.avatar = data.get("avatar")

    user.save()
    return user, None