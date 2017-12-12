from itertools import chain
import configparser, os
from django.conf import settings

def get_multichain_info():
	'''fetches multichain username, password and port only if multichain is installed with default settings'''
	chain_name = settings.CHAIN_NAME
	chain_info = {}
	# note that since multichain is installed for local user, no root access required
	paramsparser = configparser.ConfigParser()
	with open(os.environ["HOME"] + "/.multichain/"+ chain_name + "/params.dat") as lines:
		lines = chain(("[top]",), lines)  # This line does the trick.
		paramsparser.read_file(lines)

	chain_info["port"] = paramsparser["top"]["default-rpc-port"].split()[0]

	credparser = configparser.ConfigParser()
	with open(os.environ["HOME"] + "/.multichain/"+ chain_name + "/multichain.conf") as lines:
		lines = chain(("[top]",), lines)  # This line does the trick.
		credparser.read_file(lines)

	chain_info["username"] = credparser["top"]["rpcuser"]
	chain_info["password"] = credparser["top"]["rpcpassword"]
	return chain_info