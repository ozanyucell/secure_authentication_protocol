import hashlib

key = 1234567890

message = "ffa16cb29ac811eeaa2e6f70923b1a4fccad55aa"

test1 = int(message, 16) ^ key

print(test1)

test2 = test1 ^ key
print(message)
print(hex(test2)[2:])
