#!/usr/bin/env python3
import random
import numpy as np
import math

def file_reader():
    with open("./secure_authentication_protocol/ID.txt", mode="r", encoding="UTF-8") as file:
        id = file.read()
    return id

def H(message):
    message_byte = bytes(str(message), 'UTF-8')
    hashed = crc16(message_byte)
    return hashed

def crc16(data: bytes):
    crc = 0xFFFF
    for b in bytearray(data):
        crc ^= (0xFF & b)
        for _ in range(0, 8):
            if (crc & 0x0001):
                crc = ((crc >> 1) & 0xFFFF) ^ 0xA001
            else:
                crc = ((crc >> 1) & 0xFFFF)

    return np.uint16(crc)

def gcd(x, y):
    while y != 0:
        x, y = y, x % y
    return x

def coprime(x, y):
    return gcd(x, y) == 1

def key_generator(p, q):
    n = p * q
    ctf = math.lcm(p-1, q-1)

    check = False
    e = 7
    while not check:
        check = coprime(ctf, e)
        if check == True:
            break
        e = e + 1

    d = pow(e, -1, ctf)
    return f"{e};{n}", f"{d};{n}"

def RSA(hashed_id, key):
    key_first = int(key.split(";")[0])
    key_second = int(key.split(";")[1])

    encrypted = (int(hashed_id) ** key_first) % key_second
    encrypted = int(hex(encrypted)[2:], 16)

    return encrypted

def session_key_generator():
    return int(str(int(random.uniform(10000, 49999))) + str(int(random.uniform(10000, 49999))))

def bitwise_xor(x, y):
    return x ^ y

def conc(list):
    return f"{list[0]};{list[1]};{list[2]}"

def source(id, private_src, public_dst):
    hashed_id = H(id)
    encrypted_id = RSA(RSA(hashed_id, private_src), public_dst)

    src_list = [int(id), encrypted_id]
    s_key = session_key_generator()
    src_list[0] = bitwise_xor(src_list[0], s_key)
    src_list[1] = bitwise_xor(src_list[1], s_key)
    print("Session Key: " + str(s_key))

    s_key_left = str(s_key)[:(len(str(s_key))//2)]
    s_key_right = str(s_key)[(len(str(s_key))//2):]

    enc_s_key = str(RSA(s_key_left, public_dst)) + "-" + str(RSA(s_key_right, public_dst))

    src_list = list(map(str, src_list))
    src_list.append(enc_s_key)
    packet = conc(src_list)

    return packet

def destination(packet, private_dst, public_src):
    src_list = packet.split(";")
    enc_s_key = src_list[2]

    enc_s_key_left = enc_s_key.split("-")[0]
    enc_s_key_right = enc_s_key.split("-")[1]

    s_key = int(str(RSA(enc_s_key_left, private_dst)) + str(RSA(enc_s_key_right, private_dst)))
    print("Returned Session Key: " + str(s_key))
    src_list[0] = bitwise_xor(int(src_list[0]), s_key)
    src_list[1] = bitwise_xor(int(src_list[1]), s_key)

    hashed_id_src = src_list[1]
    decrypted_hash = RSA(RSA(hashed_id_src, private_dst), public_src)

    return decrypted_hash

def verify(Hash_sent, Hash_computed):
    if str(Hash_sent) == str(Hash_computed):
        print("Verified")
    else:
        print("Verification Failed")

def main():
    public_src, private_src = key_generator(5501, 4481)
    public_dst, private_dst = key_generator(6733, 6073)

    id = file_reader()

    print("-"*42)
    print("Original ID: " + str(id))

    print("-"*42)
    print("Source Public Key: {" + str(public_src) + "}")
    print("Source Private Key: {" + str(private_src) + "}")
    print("Destination Public Key: {" + str(public_dst) + "}")
    print("Destination Private Key: {" + str(private_dst) + "}")
    print("-"*42)

    source_packet = source(id, private_src, public_dst)

    hash_computed = destination(source_packet, private_dst, public_src)
    print("-"*42)
    print("Original Hashed ID (CRC-16/MODBUS): " + str(hex(H(id))))
    print("Computed Hash: " + str(hex(hash_computed)))
    print("-"*42)
    verify(H(id), hash_computed)
    print("-"*42)

if __name__ == "__main__":
    main()
