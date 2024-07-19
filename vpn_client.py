import socket
from Crypto.Cipher import AES
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
import base64

# Key generation function
def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password))

# Encrypt function
def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce + ciphertext

# Decrypt function
def decrypt(data, key):
    nonce = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    
    password = b'my_very_secure_password'
    salt = client.recv(16)  # Receive salt from server
    key = generate_key(password, salt)
    
    while True:
        message = input("Enter message: ")
        encrypted_message = encrypt(message.encode('utf-8'), key)
        client.send(encrypted_message)
        encrypted_response = client.recv(1024)
        response = decrypt(encrypted_response, key)
        print(f"Server response: {response.decode('utf-8')}")

if __name__ == '__main__':
    main()
