import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

FERNET_SECRET: bytes = os.getenv("FERNET_SECRET_KEY").encode()
fernet = Fernet(FERNET_SECRET)


def encrypt_api_key(api_key: str) -> str:
    return fernet.encrypt(api_key.encode()).decode()


def decrypt_api_key(encrypted: str) -> str:
    return fernet.decrypt(encrypted.encode()).decode()


def encrypt_email(email: str) -> str:
    return fernet.encrypt(email.encode()).decode()


def decrypt_email(encrypted: str) -> str:
    return fernet.decrypt(encrypted.encode()).decode()
