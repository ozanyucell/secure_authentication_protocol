#!/usr/bin/env python3

import hashlib

def sha1(id):
    hashed = hashlib.sha1(bytes(f"{id}",encoding="utf-8")).hexdigest()
    return hashed

def concatenate(id, hashed):
    return f"{id};{hashed}"

def key_generator():
    # select prime numbers
    p=17
    q=11
    e=7
    n = p * q

    phi = (p-1) * (q-1)

    while(e<phi):
        if (GCD(e,phi)==1):
            break
        e+=1
        
    d = pow(e, -1, phi)

    public_key = f"{e}, {n}"
    private_key = f"{d}, {n}"
    
    return "Private: {" + private_key + "}\nPublic: {" + public_key  + "}"

def GCD(x, y):
    while y != 0:
        x, y = y, x % y
    return x

def main():
    with open("./secure_authentication_protocol/ID.txt", mode="r", encoding="UTF-8") as file:
        id = file.read()
    hashed = sha1(id)

if __name__ == "__main__":
    main()
