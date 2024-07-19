import socket
import threading
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
import base64
import os

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

# Handle client connections
def handle_client(client_socket, key):
    while True:
        encrypted_data = client_socket.recv(1024)
        if not encrypted_data:
            break
        data = decrypt(encrypted_data, key)
        print(f"Received: {data.decode('utf-8')}")
        response = f"Server received: {data.decode('utf-8')}"
        encrypted_response = encrypt(response.encode('utf-8'), key)
        client_socket.send(encrypted_response)
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")

    password = b'my_very_secure_password'
    salt = os.urandom(16)
    key = generate_key(password, salt)

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_socket.send(salt)  # Send salt to client for key generation
        client_handler = threading.Thread(target=handle_client, args=(client_socket, key))
        client_handler.start()

if __name__ == '__main__':
    main()
