import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve keys from environment variables safely
API_KEY = os.getenv("GOOGLE_API_KEY")
encryption_key_env = os.getenv("ENCRYPTION_KEY")

if API_KEY is None or encryption_key_env is None:
    raise ValueError("Missing GOOGLE_API_KEY or ENCRYPTION_KEY in .env file.")

# Tell the type checker these are definitely strings now
assert isinstance(API_KEY, str)
assert isinstance(encryption_key_env, str)

# Initialize the Fernet instance once globally for efficiency
try:
    _fernet_instance = Fernet(encryption_key_env.encode())
except Exception as _err:
    raise ValueError(f"Invalid ENCRYPTION_KEY format: {_err}")

def encrypt_api_key() -> bytes:
    """
    Encrypts the loaded Google API key.
    
    Returns:
        bytes: The encrypted token representing the API key.
    """
    assert isinstance(API_KEY, str)
    return _fernet_instance.encrypt(API_KEY.encode())

def decrypt_api_key(token: bytes) -> str:
    """
    Decrypts the given token to reveal the original string.
    
    Args:
        token (bytes): The encrypted token.
        
    Returns:
        str: The decrypted API key in plain text.
    """
    return _fernet_instance.decrypt(token).decode()

if __name__ == "__main__":
    encrypted_token = encrypt_api_key()
    print("Encrypted Token:", encrypted_token)
    decrypted = decrypt_api_key(encrypted_token)
    print("Decrypted Match:", decrypted == API_KEY)
