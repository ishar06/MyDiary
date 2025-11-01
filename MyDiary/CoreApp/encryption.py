from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models
import base64

class EncryptedTextField(models.TextField):
    description = "Encrypted text field"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_encryption_key(self):
        # Get or generate a key from Django settings
        key = getattr(settings, 'ENCRYPTION_KEY', None)
        if key is None:
            # Generate a new key if none exists
            key = Fernet.generate_key()
            # You should save this key somewhere secure!
        return key

    def get_fernet(self):
        return Fernet(self.get_encryption_key())

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            f = self.get_fernet()
            decrypted = f.decrypt(value.encode())
            return decrypted.decode()
        except Exception:
            # If decryption fails, return the raw value
            # This handles the case of existing, unencrypted data
            return value

    def to_python(self, value):
        if value is None:
            return value
        try:
            f = self.get_fernet()
            decrypted = f.decrypt(value.encode())
            return decrypted.decode()
        except Exception:
            # If decryption fails, return the raw value
            return value

    def get_prep_value(self, value):
        if value is None:
            return value
        f = self.get_fernet()
        # Only encrypt if the value isn't already encrypted
        try:
            # Try to decrypt - if it works, it's already encrypted
            f.decrypt(value.encode())
            return value
        except Exception:
            # If decryption fails, encrypt the value
            return f.encrypt(str(value).encode()).decode()