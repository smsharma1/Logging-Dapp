from Crypto.PublicKey import RSA
import os
import getpass
# secret_code = getpass.getpass("Please enter your cc password to protect the key\n")
secret_code = "temp"
key = RSA.generate(2048,os.urandom)
encrypted_key = key.exportKey(passphrase=secret_code, pkcs=8,
                              protection="scryptAndAES128-CBC")

file_out = open("rsa_key.bin", "wb")
file_out.write(encrypted_key)

print(key.publickey().exportKey())
