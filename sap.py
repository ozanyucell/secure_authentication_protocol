#!/usr/bin/env python3

import hashlib
import random

def sha1(id):
    hashed = hashlib.sha1(bytes(f"{id}",encoding="utf-8")).hexdigest()
    return hashed

def conc(x, y):
    return f"{x};{y}"

def session_key_generator():
    return int(random.uniform(1000000000, 9999999999))

def key_generator():
    # select prime numbers
    p=25423
    q=29633
    e=2
    n = p * q
    phi = (p-1) * (q-1)

    while (e<phi):
        if (GCD(e,phi)==1):
            break
        e+=1

    d = pow(e, -1, phi)

    public_key = f"{e};{n}"
    private_key = f"{d};{n}"
    
    return public_key, private_key

def GCD(x, y):
    while y != 0:
        x, y = y, x % y
    return x

def RSA(key, hashed_id):
    return (int(hashed_id, 16) ** int(key.split(";")[0])) % int(key.split(";")[1])

def main():
    with open("./secure_authentication_protocol/ID.txt", mode="r", encoding="UTF-8") as file:
        id = file.read()

    hashed = sha1(id)
    public_key, private_key = key_generator()

    k_h = str(int(public_key.split(";")[0]) ^ int(private_key.split(";")[0])) + ";" + private_key.split(";")[1]

    cipher_id = hex(RSA(k_h, hashed))[2:]

    print(hashed)
    print(str(public_key) + " ^ " + str(private_key) + " = " + str(k_h))
    print(cipher_id)

if __name__ == "__main__":
    main()
