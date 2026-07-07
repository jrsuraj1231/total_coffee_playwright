"""Symmetric encryption for secrets (e.g. passwords) stored in test-data files.

Uses Fernet (AES-128-CBC + HMAC) from the `cryptography` package. The key
is read from the ENCRYPTION_KEY environment variable; generate one with
`Encryptor.generate_key()` and store it as a CI secret, never in source
control alongside the encrypted data.
"""
import os

from cryptography.fernet import Fernet


class Encryptor:
    def __init__(self, key: str | None = None):
        key = key or os.getenv("ENCRYPTION_KEY")
        if not key:
            raise ValueError(
                "No encryption key provided. Set ENCRYPTION_KEY env var or pass key= explicitly."
            )
        self._fernet = Fernet(key.encode() if isinstance(key, str) else key)

    @staticmethod
    def generate_key() -> str:
        return Fernet.generate_key().decode()

    def encrypt(self, plaintext: str) -> str:
        return self._fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, token: str) -> str:
        return self._fernet.decrypt(token.encode()).decode()
