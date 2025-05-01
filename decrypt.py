from Crypto.Cipher import AES
import os

KEYFILE = "keyfile.txt"

def unpad(data):
    return data.rstrip(b"\0")

def decrypt_file(filepath, key):
    with open(filepath, 'rb') as f:
        encrypted = f.read()
    iv = encrypted[:16]
    ciphertext = encrypted[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext))
    with open(filepath, 'wb') as f:
        f.write(plaintext)

def decrypt_directory():
    with open(KEYFILE, 'r') as f:
        for line in f:
            path, hex_key = line.strip().split(',')
            key = bytes.fromhex(hex_key)
            decrypt_file(path, key)

decrypt_directory()
print("✅ All files decrypted!")
