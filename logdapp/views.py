# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import NameForm, GradeForm
from django.shortcuts import render
from django.conf import settings
from django.db import connection
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
	return render(request,'logdapp/index.html')


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


	return render(request,"logdapp/index.html")

def get_grades(request):
	try:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM logdapp_student_{}_view".format(settings.STUDENT_ID))
		rows = cursor.fetchall()
		return render(request,"logdapp/viewgrades.html",{'data':rows})
	except:
		return render(request,"logdapp/error.html")

def update_grades(request):
	form_class = GradeForm
	if request.method == 'POST':
		form = form_class(data=request.POST)
		if form.is_valid():
			Rollnumber = request.POST.get('RollNumber', '')
			Course = request.POST.get('Course', '')
			Grade = request.POST.get('Grade', '')
		else:
			return render(request,"logdapp/error.html")
		try:
			# return HttpResponse("UPDATE logdapp_prof_{}_view SET Grade = '{}' WHERE Student_ID_id={} AND Course_ID_id='{}'".format(settings.PROF_ID,Grade,Rollnumber,Course))
			cursor = connection.cursor()
			cursor.execute("UPDATE logdapp_prof_{}_view SET Grade = '{}' WHERE Student_ID_id={} AND Course_ID_id='{}'".format(settings.PROF_ID,Grade,Rollnumber,Course))
			cursor.execute("SELECT * FROM logdapp_prof_{}_view".format(settings.PROF_ID))
			rows = cursor.fetchall()
			return render(request,"logdapp/viewgrades.html",{'data':rows,'form':form_class})
		except:
			 return render(request,"logdapp/error.html")
	elif request.method == 'GET':
		try:
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM logdapp_prof_{}_view".format(settings.PROF_ID))
			rows = cursor.fetchall()
			return render(request,"logdapp/viewgrades.html",{'data':rows,'form':form_class})
		except:
			return render(request,"logdapp/error.html")
