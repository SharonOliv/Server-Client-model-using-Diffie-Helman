import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import socket
import pickle
import base64

# Diffie-Hellman Key Exchange Implementation
def diffie_hellman(p, g, private_key):
    return pow(g, private_key, p)

def compute_shared_key(public_key, private_key, p):
    return pow(public_key, private_key, p)

# AES Encryption
def encrypt_message(shared_key, plaintext):
    key = shared_key.to_bytes(16, 'big')[:16]  # AES requires a 16-byte key
    cipher = AES.new(key, AES.MODE_CBC, iv=b'1234567812345678')
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return ciphertext

# AES Decryption
def decrypt_message(shared_key, ciphertext):
    key = shared_key.to_bytes(16, 'big')[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv=b'1234567812345678')
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
    return plaintext

def server_program():
    server_socket = socket.socket()
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)
    print("Server waiting for connection...")

    conn, addr = server_socket.accept()
    print("Connected to:", addr)

    client_public_key = int(conn.recv(1024).decode())
    p = int(input("Enter a prime number (p): "))
    g = int(input("Enter a primitive root (g): "))

    server_private_key = secrets.randbelow(p - 1) + 1
    server_public_key = diffie_hellman(p, g, server_private_key)

    conn.send(str(server_public_key).encode())
    shared_key = compute_shared_key(client_public_key, server_private_key, p)
    print("Shared key established:", shared_key)

    encrypted_message = pickle.loads(conn.recv(1024))
    print("Received Encrypted Message:", encrypted_message)
    
    decrypted_message = decrypt_message(shared_key, encrypted_message)
    print("Decrypted Message from Client:", decrypted_message)
    reply = input("Enter reply message: ")
    encrypted_reply = encrypt_message(shared_key, reply)
    
    print("Encrypted Reply Sent:", encrypted_reply)
    conn.send(pickle.dumps(encrypted_reply))

    conn.close()

if __name__ == "__main__":
    server_program()
