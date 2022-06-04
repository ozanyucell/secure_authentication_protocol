#!/usr/bin/env python3

import hashlib

def sha1(id):
    hashed = hashlib.sha1(bytes(f"{id}",encoding="utf-8")).hexdigest()

    return hashed

def main():
    with open("./secure_authentication_protocol/ID.txt", mode="r", encoding="UTF-8") as file:
        id = file.read()
    hashed = sha1(id)


if __name__ == "__main__":
    main()
