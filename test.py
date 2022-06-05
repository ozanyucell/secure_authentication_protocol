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

def RSA(hashed_id, key):
    key_first = int(key.split(";")[0])
    key_second = int(key.split(";")[1])

    encrypted = (int(hashed_id) ** key_first) % key_second
    encrypted = int(hex(encrypted)[2:], 16)

    return encrypted

with open("./secure_authentication_protocol/ID.txt", mode="r", encoding="UTF-8") as file:
    id = file.read()

public_src, private_src = key_generator(17, 11)
public_dst, private_dst = key_generator(47, 31)

test = RSA(id, private_src)
print(test)
print(RSA(test, public_src))
