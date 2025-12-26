from app.models.user import User
from peewee import DoesNotExist

def login_with_google(google_info: dict):
    print(google_info)
    email = google_info["email"]
    google_id = google_info["sub"]
    name = google_info.get("name")
    avatar = google_info.get("picture")

    try:
        user = User.get(User.email == email)
    except DoesNotExist:
        user = User.create(
            email=email,
            google_id=google_id,
            name=name,
            avatar=avatar
        )

    return user
