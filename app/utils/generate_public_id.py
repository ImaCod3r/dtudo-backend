import string
import random

def generate_public_id(prefix):
    characters = string.ascii_letters + string.digits
    public_id = ''.join(random.choice(characters) for _ in range(8))
    return f"{prefix}_{public_id}"