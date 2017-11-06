from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import os
import getpass
secret_code = getpass.getpass("Please enter your cc password to protect the key\n")

key = RSA.generate(2048,os.urandom)
encrypted_key = key.exportKey(passphrase=secret_code, pkcs=8,
                              protection="scryptAndAES128-CBC")
message = "HEY My name is shubham".encode()
h = SHA256.new(message)
encrypt = pkcs1_15.new(key).sign(h)
print(encrypt)
h = SHA256.new(message)
try:
    pkcs1_15.new(key).verify(h, encrypt)
    print("The signature is valid.")
except (ValueError, TypeError):
    print("The signature is not valid.")