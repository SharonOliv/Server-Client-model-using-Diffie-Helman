#Key Exchange

import random
def diffie_hellman(n, g, private_a, private_b):
    public_a = (g, private_a)%n
    public_b = (g, private_b)% n
    
    shared_secret_a = (public_b,private_a)%n
    shared_secret_b = (public_a,private_b)%n
    
    return public_a, public_b, shared_secret_a, shared_secret_b

try:
    n = int(input("Enter a prime number (n): "))
    g = int(input("Enter a primitive root modulo (g): "))
    
    private_a = random.randint(1, n-1)
    private_b = random.randint(1, n-1)
    
    public_a, public_b, shared_secret_a, shared_secret_b = diffie_hellman(n, g, private_a, private_b)
    
    print("Private key of A (x):", private_a)
    print("Private key of B (y):", private_b)
    print("Public key of A (k1):", public_a)
    print("Public key of B (k2):", public_b)
    print("Shared secret key computed by A (k1^y):", shared_secret_a)
    print("Shared secret key computed by B (k2^x):", shared_secret_b)
    
    assert shared_secret_a == shared_secret_b, "Error: Shared secret keys do not match!"
    print("Key exchange successful!")
except ValueError:
    print("Invalid input! Please enter integer values.")
