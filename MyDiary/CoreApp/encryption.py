from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models

class EncryptedTextField(models.TextField):
    """
    A custom TextField that encrypts data before saving to database and decrypts when retrieving.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_encryption_key(self):
        key = getattr(settings, 'ENCRYPTION_KEY', None)
        if key is None:
            key = Fernet.generate_key()
        return key

    def get_fernet(self):
        return Fernet(self.get_encryption_key())

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            # Try to decrypt if it looks like base64
            try:
                value.encode('ascii')
                f = self.get_fernet()
                # If this succeeds, it was encrypted
                decrypted = f.decrypt(value.encode())
                return decrypted.decode()
            except UnicodeEncodeError:
                # If we can't encode as ASCII, it's probably not encrypted
                return value
        except:
            # If decryption fails, it wasn't encrypted
            return value

    def to_python(self, value):
        return value

    def get_prep_value(self, value):
        if value is None:
            return value
        # Don't encrypt if it's already encrypted
        try:
            # Try to decrypt - if it works, it's already encrypted
            f = self.get_fernet()
            try:
                f.decrypt(str(value).encode())
                return value
            except:
                # If decryption fails, encrypt it
                return f.encrypt(str(value).encode()).decode()
        except:
            # If there's any error, encrypt the value
            f = self.get_fernet()
            return f.encrypt(str(value).encode()).decode()
        # Only encrypt if the value isn't already encrypted
        try:
            # Try to decrypt - if it works, it's already encrypted
            f.decrypt(value.encode())
            return value
        except Exception:
            # If decryption fails, encrypt the value
            return f.encrypt(str(value).encode()).decode()