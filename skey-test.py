import math
import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def coprime(a, b):
    return gcd(a, b) == 1

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

public_dst, private_dst = key_generator(6733, 6073)
print(f"Public Key: {public_dst}")
print(f"Private Key: {private_dst}")
print("-"*50)
s_key = session_key_generator()
print(f"Session Key: {s_key}")

# ENCRYPTION
s_key_left = str(s_key)[:(len(str(s_key))//2)]
s_key_right = str(s_key)[(len(str(s_key))//2):]
print(f"Left Session Key: {s_key_left} | Right Session Key: {s_key_right}")

zero_incident = False
if s_key_right.startswith("0"): 
    zero_incident = True

if zero_incident == False:
    enc_s_key = int(str(RSA(s_key_left, public_dst)) + str(RSA(s_key_right, public_dst)))
else:
    enc_s_key = int(str(RSA(s_key_left, public_dst)) + "0" + str(RSA(s_key_right, public_dst)))

# DECRYPTION
enc_s_key_left = str(enc_s_key)[:(len(str(enc_s_key))//2)]
enc_s_key_right = str(enc_s_key)[(len(str(enc_s_key))//2):]
print(f"Left Session Key: {enc_s_key_left} | Right Session Key: {enc_s_key_right}")

zero_incident = False
if enc_s_key_right.startswith("0"): 
    zero_incident = True

if zero_incident == False:
    s_key = int(str(RSA(enc_s_key_left, private_dst)) + str(RSA(enc_s_key_right, private_dst)))
else:
    s_key = int(str(RSA(enc_s_key_left, private_dst)) + "0" +  str(RSA(enc_s_key_right, private_dst)))

print(f"s_key: {s_key}")
print("-"*50)
