import base64
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def generate_vapid():
    private_key = ec.generate_private_key(ec.SECP256R1())
    
    # Private Key to Int
    private_val = private_key.private_numbers().private_value
    private_bytes = private_val.to_bytes(32, byteorder='big')
    private_b64 = base64.urlsafe_b64encode(private_bytes).decode('utf-8').rstrip('=')
    
    # Public Key (Uncompressed format: 0x04 + X + Y)
    public_val = private_key.public_key().public_numbers()
    x = public_val.x.to_bytes(32, byteorder='big')
    y = public_val.y.to_bytes(32, byteorder='big')
    
    public_bytes = b'\x04' + x + y
    public_b64 = base64.urlsafe_b64encode(public_bytes).decode('utf-8').rstrip('=')
    
    print(f"VAPID_PRIVATE_KEY={private_b64}")
    print(f"VAPID_PUBLIC_KEY={public_b64}")
    print(f"VAPID_CLAIMS_EMAIL=mailto:admin@gesttec.com")

if __name__ == "__main__":
    generate_vapid()
