#!/usr/bin/env python3

import hashlib

def sha1(id):
    hashed = hashlib.sha1(bytes(f"{id}",encoding="utf-8"))
    pbHash = hashed.hexdigest()

    print(hashed)
    print(pbHash)
    print("ffa16cb29ac811eeaa2e6f70923b1a4fccad55aa")

def main():
    with open("./secure_authentication_protocol/ID.txt", mode="r", encoding="UTF-8") as file:
        id = file.read()
    sha1(id)


if __name__ == "__main__":
    main()
