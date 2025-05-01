from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

KEYFILE = "keyfile.txt"

def pad(data):
    return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

def encrypt_file(filepath, key):
    with open(filepath, 'rb') as f:
        plaintext = f.read()
    plaintext = pad(plaintext)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = iv + cipher.encrypt(plaintext)
    with open(filepath, 'wb') as f:
        f.write(encrypted)

def encrypt_directory():
    key = get_random_bytes(32)
    with open(KEYFILE, 'w') as f:
        for dirpath, _, filenames in os.walk("critical"):
            for name in filenames:
                path = os.path.join(dirpath, name)
                encrypt_file(path, key)
                f.write(f"{path},{key.hex()}\n")

encrypt_directory()
print("✅ All files encrypted!")
