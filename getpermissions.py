#!/usr/bin/python
import requests
from sys import stdin
import sys, os
import json
from Savoir import Savoir
import getpass, configparser
from itertools import chain
from Crypto.PublicKey import RSA

def send_data(user, passwd, addr, publickey):
	querydata = {
		'key': str(addr),
		'user': str(user),
		'password': str(passwd),
		'publickey': publickey.decode(),
	}
	payload = json.dumps(querydata)
	# pass an https url here for security, this one is dummy
	url = "http://192.168.0.103:8000/logdapp/grantpermissions/"
	# url = "http://172.24.0.30:8000/logdapp/grantpermissions/"
	url = "http://localhost:8000/logdapp/grantpermissions/"
	response = requests.request("POST", url, data=payload, verify=False)
	return response

def main(argv):
	user = input("OARS Username:")
	passwd = getpass.getpass("Password for " + user + ":")
	encryption_pass = "temp"

	encoded_key = open("rsa_key"+"_prof"+user+".bin", "rb").read()
	key = RSA.import_key(encoded_key, passphrase=str(encryption_pass))

	clientchain = "chain1"
	paramsparser = configparser.ConfigParser()
	with open(os.environ["HOME"] + "/.multichain/"+ clientchain + "/params.dat") as lines:
		lines = chain(("[top]",), lines)  # This line does the trick.
		paramsparser.read_file(lines)

	clientport = paramsparser["top"]["default-rpc-port"].split()[0]

	credparser = configparser.ConfigParser()
	with open(os.environ["HOME"] + "/.multichain/"+ clientchain + "/multichain.conf") as lines:
		lines = chain(("[top]",), lines)  # This line does the trick.
		credparser.read_file(lines)

	clientuser = credparser["top"]["rpcuser"]
	clientpass = credparser["top"]["rpcpassword"]
	print(clientuser, clientpass, "localhost", clientport, clientchain)
	api = Savoir(clientuser, clientpass, "localhost", clientport, clientchain)

	data = api.getaddresses()
	# print(data)
	# data = api.liststreams()
	# print(data)

	response = send_data(user, passwd, data[0], key.publickey().exportKey())
	print(response)
	if(response.status_code == 200):		
		api.subscribe("logstream")

if __name__ == "__main__":
   main(sys.argv[1:])
