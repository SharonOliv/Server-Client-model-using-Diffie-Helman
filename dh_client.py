import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import socket
import pickle

# Diffie-Hellman Key Exchange Implementation
def diffie_hellman(p, g, private_key):
    return (g, private_key)%p

def compute_shared_key(public_key, private_key, p):
    return (public_key, private_key)%p

# AES Encryption
def encrypt_message(shared_key, plaintext):
    key = shared_key.to_bytes(16, 'big')[:16]  # AES requires a 16-byte key
    cipher = AES.new(key, AES.MODE_CBC, iv=b'1234567812345678')
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return ciphertext

# AES Decryption
def decrypt_message(shared_key, ciphertext):
    key = shared_key.to_bytes(16,'big')[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv=b'1234567812345678')
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
    return plaintext

def client_program():
    client_socket = socket.socket()
    client_socket.connect(('localhost', 5000))

    p = int(input("Enter a prime number (p): "))
    g = int(input("Enter a primitive root (g): "))

    client_private_key = secrets.randbelow(p - 1) + 1
    client_public_key = diffie_hellman(p, g, client_private_key)

    client_socket.send(str(client_public_key).encode())
    server_public_key = int(client_socket.recv(1024).decode())

    shared_key = compute_shared_key(server_public_key, client_private_key, p)
    print("Shared key established:", shared_key)

    plaintext = input("Enter message to encrypt: ")
    encrypted_message = encrypt_message(shared_key, plaintext)
    
    print("Encrypted Message Sent:", encrypted_message)
    client_socket.send(pickle.dumps(encrypted_message))
    encrypted_reply = pickle.loads(client_socket.recv(1024))
    print("Received Encrypted Reply:", encrypted_reply)
    
    decrypted_reply = decrypt_message(shared_key, encrypted_reply)
    print("Decrypted Reply from Server:", decrypted_reply)
    client_socket.close()

if __name__ == "__main__":
    client_program()
