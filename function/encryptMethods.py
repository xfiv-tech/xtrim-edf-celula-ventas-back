from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import pickle
import base64


from dotenv import load_dotenv
import os

key = b'_\x18N\x92\xa8\x07\x90\xd43\x8f\xfe5#\xa0&\xd5'
iv = b'\nS/\x84\xbfeZ\xbdG\x9f\xcaW\xe8\xa1\xb3\xe4'


def encrypt_object(obj):
    # Convertir el objeto a bytes
    obj_bytes = pickle.dumps(obj)
    
    # Añadir relleno a los datos
    padded_data = pad(obj_bytes, AES.block_size)
    
    # Crear el objeto de cifrado en modo CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Cifrar los datos
    encrypted_data = cipher.encrypt(padded_data)
    
    # Devolver los datos cifrados en base64 para facilitar el transporte
    return base64.b64encode(iv + encrypted_data).decode()


def decrypt_object(encrypted_data):
    # Decodificar los datos cifrados en base64
    encrypted_data = base64.b64decode(encrypted_data)
    
    # Extraer el IV de los datos cifrados
    iv = encrypted_data[:AES.block_size]
    
    # Crear el objeto de cifrado en modo CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Descifrar los datos (ignorando el IV en los datos cifrados)
    decrypted_data = cipher.decrypt(encrypted_data[AES.block_size:])
    
    # Eliminar el relleno de los datos descifrados
    unpadded_data = unpad(decrypted_data, AES.block_size)
    
    # Convertir los datos descifrados de bytes a objeto Python
    obj = pickle.loads(unpadded_data)
    
    return obj
