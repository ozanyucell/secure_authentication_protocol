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

def source(private_src, public_dst):

    with open("./secure_authentication_protocol/ID.txt", mode="r", encoding="UTF-8") as file:
        id = file.read()
    hashed = sha1(id)
    hashed = int(hashed, 16)

    k_h = str(int(public_dst.split(";")[0]) ^ int(private_src.split(";")[0])) + ";" + str(int(public_dst.split(";")[1]) ^ int(private_src.split(";")[1]))
    cipher_id = RSA(hashed, k_h)

    concatenated_id = f"{id}{cipher_id}"

    s_key = session_key_generator()
    s_key = f"{str(s_key)[:5]};{str(s_key)[5:]}"

    cipher = RSA(concatenated_id, s_key)

    s_key = s_key.split(";")[0] + s_key.split(";")[1]
    print(s_key)
    cipher_key = RSA(s_key, public_dst)
    packet = f"{cipher};{cipher_key}"

    return packet


def destination(private_dst, public_src, packet):
    hashed_id_src = packet.split(";")[0]
    cipher_key_src = packet.split(";")[1]

    session_key = RSA(cipher_key_src, private_dst)
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
    public_src, private_src = key_generator(17, 11)
    public_dst, private_dst = key_generator(47, 31)

    source_packet = source(private_src, public_dst)
    #print(source_packet)
    
    destination(private_dst, public_src, source_packet)

if __name__ == "__main__":
    main()
