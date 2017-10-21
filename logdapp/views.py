# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .forms import NameForm
from django.shortcuts import render
from Savoir import Savoir
import json
from itertools import chain
import configparser
import os

rpcuser = 'multichainrpc'
# rpcpasswd = 'BWVjg5eJJgvJbgNQL9iaoHBwLLapx369ZeWxRZHVhWAR'
rpcpasswd = 'FQ8oQx4Y3fFu9zc1chprrmWXH9gP1qRqpxBnVi7QneCL'
rpchost = 'localhost'
rpcport = '8338'
chainname = 'demo'

api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)

def index(request):
	return HttpResponse("Hello, world. You're at the polls index.")


def get_name(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = NameForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			return HttpResponse(json.dumps(api.getinfo(), indent=4, sort_keys=True))

	# if a GET (or any other method) we'll create a blank form
	else:
		form = NameForm()

	return render(request, 'logdapp/name.html', {'form': form})

@csrf_exempt
def grant_permissions(request):
	# my server runs on docker
	serverchain = "chain1"

	# note that since multichain is installed for local user, no root access required
	paramsparser = configparser.ConfigParser()
	with open(os.environ["HOME"] + "~/.multichain/"+ clientchain + "/params.dat") as lines:
		lines = chain(("[top]",), lines)  # This line does the trick.
		paramsparser.read_file(lines)

	serverport = paramsparser["top"]["default-rpc-port"].split()[0]

	credparser = configparser.ConfigParser()
	with open(os.environ["HOME"] + "/.multichain/chain1/multichain.conf") as lines:
		lines = chain(("[top]",), lines)  # This line does the trick.
		credparser.read_file(lines)
			
	serveruser = credparser["rpcuser"]
	serverpass = credparser["rpcpassword"]
	api = Savoir(serveruser, serverpass, "localhost", serverport, serverchain)

	if request.method == 'POST':
		for key, value in request.POST.lists():
			print("%s %s" % (key, value))
		key = json.loads(request.body)["key"]
		print(key)
		api.grant(str(key), logstream.write)
		return HttpResponse("Successfully received data")
	else:
		return HttpResponse("Please send a post request with key")

def client_view(request):
	# to do change chain name dynamically
	clientchain = "chain1"
	paramsparser = configparser.ConfigParser()
	with open(os.environ["HOME"] + "~/.multichain/"+ clientchain + "/params.dat") as lines:
		lines = chain(("[top]",), lines)  # This line does the trick.
		paramsparser.read_file(lines)

	clientport = paramsparser["top"]["default-rpc-port"].split()[0]

	credparser = configparser.ConfigParser()
	with open(os.environ["HOME"] + "/.multichain/chain1/multichain.conf") as lines:
		lines = chain(("[top]",), lines)  # This line does the trick.
		credparser.read_file(lines)

	clientuser = credparser["rpcuser"]
	clientpass = credparser["rpcpassword"]
	api = Savoir(clientuser, clientpass, "localhost", clientport, clientchain)


