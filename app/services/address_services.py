from app.models.address import Address
from app.models.user import User

def create_address(user_id, name, long, lat):
    address = Address.get_or_none((Address.name == name) & (Address.long == long) & (Address.lat == lat))
    
    if address:
        return address

    user = User.get_or_none(User.id == user_id)
    
    new_address = Address.create(
        name=name,
        long=long,
        lat=lat,
        user=user
    )

    return new_address

def get_addresses(user_id):
    user = User.get_by_id(user_id)
    
    addresses = Address.select().where(Address.user == user)
    
    if not addresses:
        return None, "Endereços não encontrados"
    
    return addresses, None

def delete(address_id):
    address = Address.get_or_none(Address.id == address_id)

    if not address:
        return None, 'Endereço não encontrado'
    
    deleted = address.delete_instance()

    return deleted, None

def get_address_by_id(address_id):
    address = Address.get_or_none(Address.id == address_id)
    if not address:
        return None, "Endereço não encontrado"
    return address, None
