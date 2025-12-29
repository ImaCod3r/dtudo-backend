from app.models.user import User

def get_user_by_id(id):
    user = User.get_or_none(User.id == id)
    return user