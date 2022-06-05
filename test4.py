import math

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def coprime(a, b):
    return gcd(a, b) == 1
    
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

print('Public Key is: ' f"[{e}, {n}]")
print('Private Key is: ' f"[{d}, {n}]")
