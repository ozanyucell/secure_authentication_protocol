import math


import math

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def coprime(a, b):
    return gcd(a, b) == 1

def key_generator():   
    p = 17
    q = 11
    n = p*q
    phi = math.lcm(p-1, q-1)

    check = False
    e = 5
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

public_src, private_src = key_generator()
#public_dst, private_dst = key_generator(127, 31)

#k_h = str(int(private_src.split(";")[0]) ^ int(public_dst.split(";")[0])) + ";" + str(int(private_src.split(";")[1]) ^ int(public_dst.split(";")[1]))

print(f"Public Key is: {public_src}")
print(f"Private Key is: {private_src}")
#print("DST Public: " + public_dst + " | SRC Private: " + private_dst)
#print(k_h)

test = RSA(id, private_src)
print(test)

#k_h2 = str(int(private_dst.split(";")[0]) ^ int(public_src.split(";")[0])) + ";" + str(int(private_dst.split(";")[1]) ^ int(public_src.split(";")[1]))
#print(k_h2)

print(RSA(test, public_src))
