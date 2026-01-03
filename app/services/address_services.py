from app.models.address import Address
from app.models.user import User

def create_address(user_id, name, long, lat):
    address = Address.get_or_none((Address.name == name) & (Address.long == long) & (Address.lat == lat))
    if address:
        return address

    user = User.get_or_none(User.id == user_id)
    if not user:
        return None

    new_address = Address.create(
        name=name,
        long=long,
        lat=lat,
        user=user
    )

    return new_address