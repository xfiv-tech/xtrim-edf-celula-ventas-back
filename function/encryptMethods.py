from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import pickle
import base64


from dotenv import load_dotenv
import os

key = b'\x86$\x02\xc9VQ\x95\x8b\\O\x7f\x00\xb3\x8e\x11a\xab\xc2\x9c\x83U\xed|\xf7\xc0?h\xba\xf0{\x97&'
def encrypt_object(obj):
    serialized_obj = pickle.dumps(obj)
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(serialized_obj, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    encrypted_data = base64.b64encode(encrypted_data).decode('utf-8')

    return encrypted_data

def decrypt_object(encrypted_data):
    encrypted_data = base64.b64decode(encrypted_data)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(encrypted_data)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    obj = pickle.loads(unpadded_data)
    
    return obj
