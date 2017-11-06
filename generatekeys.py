import os
from Crypto.PublicKey import RSA
from Crypto import Random

rng = Random.new().read
RSAkey = RSA.generate(1024, rng) 

privatekey = RSAkey
publickey = RSAkey.publickey()
print(privatekey.exportKey()) #export under the 'PEM' format (I think)
print(publickey.exportKey())

file = open("PublicKey.txt", "wb")
file.write(publickey.exportKey())
file.close()
file = open("PrivateKey.txt", "wb")
file.write(privatekey.exportKey()) #save exported private key
file.close()