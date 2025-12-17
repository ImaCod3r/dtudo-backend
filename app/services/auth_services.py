from app.models.user import User

def login_with_google(google_info):
    user, created = User.get_or_create(
        google_id=google_info["sub"],
        defaults={
            "email": google_info["email"],
            "name": google_info["name"],
            "avatar": google_info.get("picture")
        }
    )
    return user