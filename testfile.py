# from cryptography.fernet import Fernet
# b=Fernet.generate_key()
# print(b)

from cryptography.fernet import Fernet
import base64
import logging
import traceback

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedSHA1PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
]
ENCRYPT_KEY = b'wa4Whw-fiYCWFZGagMBT9su62KI-JOoj4aamftCz4Rc='


# function for encrypt the text

def encrypt(text):
    try:
        pas = str(text)
        cipher_pass = Fernet(ENCRYPT_KEY)
        encrypt_pass = cipher_pass.encrypt(pas.encode('ascii'))
        encrypt_pass = base64.urlsafe_b64encode(encrypt_pass).decode("ascii")
        return encrypt_pass
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


# function for decrypt the encrypted text

def decrypt(text):
    try:
        pas = base64.urlsafe_b64decode(text)
        cipher_pass = Fernet(ENCRYPT_KEY)
        decod_pass = cipher_pass.decrypt(pas).decode("ascii")
        return decod_pass
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


p = encrypt('Jikku@123')
print(p)
d = decrypt(
    'Z0FBQUFBQmtnVjRlbTBYbnNjQnk3WmFfNkJyTldwN1l3U3VnVnNqa25BbUg0MTd4d1RQY2g5MVNXc3JSQVI5aTE4SWdZemlDYnRJbGJWejNDRWdDaHZXU1JsQjMtNEZTcUE9PQ==')
print(d)
