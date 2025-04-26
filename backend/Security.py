from cryptography.fernet import Fernet
import os

FERNET_SECRET: bytes = os.getenv("FERNET_SECRET_KEY").encode()
fernet = Fernet(FERNET_SECRET)


def encrypt_api_key(api_key: str) -> str:
    return fernet.encrypt(api_key.encode()).decode()


def decrypt_api_key(encrypted: str) -> str:
    return fernet.decrypt(encrypted.encode()).decode()
