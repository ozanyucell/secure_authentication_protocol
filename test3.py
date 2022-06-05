import random

def session_key_generator():
    return int(random.uniform(1000000000, 9999999999))

def key_generator(p, q):
    e=7
    n = p * q
    phi = (p-1) * (q-1)

    while (e<phi):
        if (GCD(e,phi)==1):
            break
        e+=1

    k = 2 # constant
    d = (1 + (k*phi)) / e
    d = int(d)
    
    public_key = f"{e};{n}"
    private_key = f"{d};{n}"
    
    return public_key, private_key

def GCD(x, y):
    while y != 0:
        x, y = y, x % y
    return x

def RSA(hashed_id, key):
    key_first = int(key.split(";")[0])
    key_second = int(key.split(";")[1])

    encrypted = (int(hashed_id) ** key_first) % key_second
    encrypted = int(hex(encrypted)[2:], 16)

    return encrypted

public_key, private_key = key_generator(17, 11)
message = session_key_generator

enc = RSA(message, private_key)

print(f"enc: {enc}")

dec = RSA(enc, public_key)

print(f"message: {message}")
print(f"dec: {dec}")
