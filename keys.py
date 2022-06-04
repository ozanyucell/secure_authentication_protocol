def key_generator():
    # select prime numbers
    p=17
    q=11
    e=7
    n = p * q

    phi = (p-1) * (q-1)

    while(e<phi):
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

public, private = key_generator()

print(public)
print(private)
