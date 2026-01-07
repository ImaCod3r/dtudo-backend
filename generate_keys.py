from py_vapid import Vapid
v = Vapid()
v.generate_keys()
print(f"Public Key: {v.public_key.decode('utf-8')}") # v.public_key is bytes?
# Actually let's check how py_vapid works or use a simpler way if possible.
# Wait, I don't want to guess the API.
# Let's use the CLI if possible.
