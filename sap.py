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

def key_generator(p, q):
    # select prime numbers
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
    key_first = int(key.split(";")[0])
    key_second = int(key.split(";")[1])

    encrypted = (int(hashed_id) ** key_first) % key_second
    encrypted = int(hex(encrypted)[2:], 16)

    return encrypted

def source(private_src, public_dst):

    with open("./secure_authentication_protocol/ID.txt", mode="r", encoding="UTF-8") as file:
        id = file.read()
    hashed = sha1(id)
    hashed = int(hashed, 16)

    k_h = str(int(public_dst.split(";")[0]) ^ int(private_src.split(";")[0])) + ";" + str(int(public_dst.split(";")[0]) ^ int(private_src.split(";")[1]))
    cipher_id = RSA(k_h, hashed)

    concatenated_id = f"{id}{cipher_id}"
    s_key = session_key_generator()
    s_key = f"{str(s_key)[:5]};{str(s_key)[5:]}"

    cipher = RSA(s_key, concatenated_id)

    s_key = s_key.split(";")[0] + s_key.split(";")[1]
    cipher_key = RSA(public_dst, s_key)
    print(cipher_key)
    packet = f"{cipher};{cipher_key}"

    return packet


def destination(private_dst, public_src):
    return 0

def main():
    public_src, private_src = key_generator(17, 11)
    public_dst, private_dst = key_generator(47, 31)

    source_packet = source(private_src, public_dst)
    print(source_packet)
    
    destination(private_dst, public_src)

if __name__ == "__main__":
    main()
