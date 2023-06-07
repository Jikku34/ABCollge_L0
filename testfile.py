from cryptography.fernet import Fernet
b=Fernet.generate_key()
print(b)