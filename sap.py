#!/usr/bin/env python3
import random
import numpy as np
import math

def crc16(data: bytes):
    data = bytearray(data)
    poly = 0xA001
    crc = 0xFFFF
    for b in data:
        crc ^= (0xFF & b)
        for _ in range(0, 8):
            if (crc & 0x0001):
                crc = ((crc >> 1) & 0xFFFF) ^ poly
            else:
                crc = ((crc >> 1) & 0xFFFF)

    return np.uint16(crc)

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def coprime(a, b):
    return gcd(a, b) == 1
####################################################
def conc(x, y):
    return f"{x};{y}"
####################################################
def session_key_generator():
    return int(random.uniform(1000000000, 9999999999))

def key_generator(p, q):
    n = p * q
    phi = math.lcm(p-1, q-1)

    check = False
    e = 17
    while not check:
        check = coprime(phi, e)
        if check == True:
            break
        e = e + 1

    d = pow(e, -1, phi)
    return f"{e};{n}", f"{d};{n}"

def RSA(hashed_id, key):
    key_first = int(key.split(";")[0])
    key_second = int(key.split(";")[1])

    encrypted = (int(hashed_id) ** key_first) % key_second
    encrypted = int(hex(encrypted)[2:], 16)

    return encrypted
####################################################
def source(private_src, public_dst):

    with open("./secure_authentication_protocol/ID.txt", mode="r", encoding="UTF-8") as file:
        id = file.read()

    id_byte = bytes(id, 'UTF-8')
    hashed = crc16(id_byte)
    
    k_h = str(int(public_dst.split(";")[0]) ^ int(private_src.split(";")[0])) + ";" + str(int(public_dst.split(";")[1]) ^ int(private_src.split(";")[1]))
    cipher_id = RSA(hashed, k_h)

    concatenated_id = f"{id}{cipher_id}"

    s_key = session_key_generator()

    #cipher = concatenated_id ^ s_key

    print(s_key)
    cipher_key = RSA(s_key, public_dst)
    print(cipher_key)
    #packet = f"{cipher};{cipher_key}"

    return cipher_key

def destination(private_dst, public_src, packet):
    # hashed_id_src = packet.split(";")[0]
    # cipher_key_src = packet.split(";")[1]

    #session_key = RSA(cipher_key_src, private_dst)
    session_key = RSA(packet, private_dst)
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
    public_src, private_src = key_generator(349, 337)
    public_dst, private_dst = key_generator(47, 31)

    source_packet = source(private_src, public_dst)
    #print(source_packet)
    
    destination(private_dst, public_src, source_packet)

if __name__ == "__main__":
    main()
