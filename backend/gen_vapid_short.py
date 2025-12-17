import base64
from cryptography.hazmat.primitives.asymmetric import ec

private_key = ec.generate_private_key(ec.SECP256R1())
private_val = private_key.private_numbers().private_value
private_b64 = base64.urlsafe_b64encode(private_val.to_bytes(32, 'big')).decode('utf-8').rstrip('=')

public_val = private_key.public_key().public_numbers()
public_bytes = b'\x04' + public_val.x.to_bytes(32, 'big') + public_val.y.to_bytes(32, 'big')
public_b64 = base64.urlsafe_b64encode(public_bytes).decode('utf-8').rstrip('=')

print(private_b64)
print(public_b64)
