import os
try:
    from cryptography.fernet import Fernet
except ImportError:
    print("Installing cryptography library...")
    os.system("pip install cryptography")
    from cryptography.fernet import Fernet

def generate_encrypted_credentials(api_key: str):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted = f.encrypt(api_key.encode())
    
    print("\n" + "="*50)
    print("✅ ENCRYPTION SUCCESSFUL!")
    print("="*50)
    print("\nCopy and paste these exact two lines into your .env file:\n")
    print(f"FERNET_KEY={key.decode()}")
    print(f"ENCRYPTED_API_KEY={encrypted.decode()}")
    print("\n" + "="*50)
    print("You can now safely push your code to Git! The plaintext AIza key is perfectly hidden.")

if __name__ == "__main__":
    print("\n--- Universal Intent Bridge Security Tool ---")
    raw_key = input("Paste your NEW Google API Key (Starts with AIza): ").strip()
    if raw_key:
        generate_encrypted_credentials(raw_key)
    else:
        print("Error: No key provided.")
