import math

import numpy as np

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

def key_generator(p, q):
    n = p*q
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

with open("./secure_authentication_protocol/ID.txt", mode="r", encoding="UTF-8") as file:
    id = file.read()

print("Original ID: " + str(id))
id_byte = bytes(id,'UTF-8')
print("ID in Bytes: " + str(id_byte))
id_hashed = crc16(id_byte)
print("Hashed ID: " + str(id_hashed))

public_src, private_src = key_generator(349, 337)
public_dst, private_dst = key_generator(383, 379)

print("SRC Public: " + public_src + " | SRC Private: " + private_src)
print("DST Public: " + public_dst + " | DST Private: " + private_dst)

k_h = str(int(public_dst.split(";")[0]) ^ int(private_src.split(";")[0])) + ";" + str(int(public_dst.split(";")[1]) ^ int(private_src.split(";")[1]))
encoded = RSA(id_hashed, k_h)
print("Encoded: " + str(encoded))

k_h2 = str(int(private_dst.split(";")[0]) ^ int(public_src.split(";")[0])) + ";" + str(int(private_dst.split(";")[1]) ^ int(public_src.split(";")[1]))
decoded = RSA(encoded, k_h)
print("Decoded: " + str(decoded))

print(f"kh: {k_h}")
print(f"kh2: {k_h2}")

if id_hashed == decoded:
    print("True KEKW.")
else:
    print("Git Gud")
