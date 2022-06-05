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

def source(private_key, public_key):

    with open("./secure_authentication_protocol/ID.txt", mode="r", encoding="UTF-8") as file:
        id = file.read()
    hashed = sha1(id)
    hashed = int(hashed, 16)

    cipher_id = RSA(hashed, private_key)

    concatenated_id = f"{id}{cipher_id}"

    s_key = session_key_generator()

    cipher = int(concatenated_id) ^ s_key

    print(s_key)

    cipher_key = RSA(s_key, private_key)

    packet = f"{cipher};{cipher_key}"

    return packet


def destination(private_key, public_key, packet):
    hashed_id_src = packet.split(";")[0]
    cipher_key_src = packet.split(";")[1]

    session_key = RSA(cipher_key_src, public_key)
    print(session_key)
    exit(0)
    enc_hashed = str(RSA(hashed_id_src, session_key))
    print(enc_hashed)

    id, hashed_id = enc_hashed.split("77777")[0], enc_hashed.split("77777")[1]

    dst_hashed = sha1(id)
    dst_hashed = int(dst_hashed, 16)

    k_h = str(int(private_dst.split(";")[0]) ^ int(public_src.split(";")[0])) + ";" + str(int(private_dst.split(";")[1]) ^ int(public_src.split(";")[1]))
    hash_val = RSA(hashed_id, k_h)

    if hash_val == dst_hashed:
        print("True")
    else:
        print("False")

def main():
    public_key, private_key = key_generator(17, 11)

    source_packet = source(private_key, public_key)
    #print(source_packet)
    
    destination(private_key, public_key, source_packet)

if __name__ == "__main__":
    main()
