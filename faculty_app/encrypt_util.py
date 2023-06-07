from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings


# function for encrypt the text

def encrypt(text):
    try:
        pas = str(text)
        cipher_pass = Fernet(settings.ENCRYPT_KEY)
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
        cipher_pass = Fernet(settings.ENCRYPT_KEY)
        decod_pass = cipher_pass.decrypt(pas).decode("ascii")
        return decod_pass
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None
