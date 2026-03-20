import unittest
import os
from dotenv import load_dotenv

# We need to make sure environment variables are loaded before secretmanager is evaluated
# Normally python-dotenv loads them automatically if dotenv is used inside the module.
# secretmanager.py calls load_dotenv() so it's safe to import.
import secretmanager

class TestSecretManager(unittest.TestCase):

    def setUp(self):
        # Ensure our env variables are present before running tests
        # We assume the .env file is populated based on our setup.
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.encryption_key = os.getenv("ENCRYPTION_KEY")
        
        # Verify setup is correct
        self.assertIsNotNone(self.api_key, "GOOGLE_API_KEY must be in .env")
        self.assertIsNotNone(self.encryption_key, "ENCRYPTION_KEY must be in .env")

    def test_encrypt_and_decrypt(self):
        """Test that a key can be successfully encrypted and decrypted back to the original value."""
        # Encrypt the API Key
        encrypted_token = secretmanager.encrypt_api_key()
        self.assertIsInstance(encrypted_token, bytes)
        self.assertNotEqual(encrypted_token, self.api_key.encode())
        
        # Decrypt it back
        decrypted_key = secretmanager.decrypt_api_key(encrypted_token)
        self.assertEqual(decrypted_key, self.api_key)

if __name__ == '__main__':
    unittest.main()
