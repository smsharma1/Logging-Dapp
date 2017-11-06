#!/usr/bin/python
import requests
from sys import stdin
import sys, os
import json
from Savoir import Savoir
import getpass, configparser
from itertools import chain


def send_data(user, passwd, addr):
	querydata = {
		'key': str(addr),
		'user': str(user),
		'password': str(passwd),
	}
	payload = json.dumps(querydata)
	# pass an https url here for security, this one is dummy
	url = "http://172.24.0.30:8000/logdapp/grantpermissions/"
	response = requests.request("POST", url, data=payload, verify=False)
	return response

def main(argv):
	user = input("OARS Username:")
	passwd = getpass.getpass("Password for " + user + ":")
	
	with open('Publickey.txt') as f:
	    selfpublickey = RSA.importKey(f.read())
    	f.close()

	# ip = argv[0];
	# port = argv[1];

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
	api = Savoir(clientuser, clientpass, "localhost", clientport, clientchain)

	data = api.getaddresses()
	print(data)
	response = send_data(user, passwd, data[0], selfpublickey.exportKey())
	print(response)
	if(response.status_code == 200):		
		api.subscribe("logstream")

if __name__ == "__main__":
   main(sys.argv[1:])