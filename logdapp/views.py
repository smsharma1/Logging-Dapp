# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import NameForm, GradeForm
from django.shortcuts import render
from django.conf import settings
from .models import User_publickey
from django.db import connection
from Savoir import Savoir
import json
from itertools import chain
import configparser
import os
import binascii

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
	with open(os.environ["HOME"] + "/.multichain/"+ serverchain + "/params.dat") as lines:
		lines = chain(("[top]",), lines)  # This line does the trick.
		paramsparser.read_file(lines)

	serverport = paramsparser["top"]["default-rpc-port"].split()[0]

	credparser = configparser.ConfigParser()
	with open(os.environ["HOME"] + "/.multichain/"+ serverchain + "/multichain.conf") as lines:
		lines = chain(("[top]",), lines)  # This line does the trick.
		credparser.read_file(lines)

	serveruser = credparser["top"]["rpcuser"]
	serverpass = credparser["top"]["rpcpassword"]
	api = Savoir(serveruser, serverpass, "localhost", serverport, serverchain)

	if request.method == 'POST':
		for key, value in request.POST.lists():
			print("%s %s" % (key, value))
		data = json.loads((request.body).decode('utf-8'))
		key = data["key"]
		user = data["user"]
		password = data["password"]
		print(data)
		# check user and password against OARS database if OK then
		# user = authenticate(username=user, password=password)
		try:
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM logdapp_user where ID_id='{}' and password='{}'".format(user,password))
			rows = cursor.fetchall()
			if rows is not None:
				api.grant(str(key), "send")
				api.grant(str(key), "logstream.write")
				cursor.execute("INSERT into logdapp_user_publickey values ('{}', {})".format(str(key),user))
				return HttpResponse("Successfully received data")
			else:
				return HttpResponse("Incorrect Username or Password")
		except:
			return render(request,"logdapp/error.html")
	else:
		return HttpResponse("Please send a post request with key")

def get_grades(request):
	try:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM logdapp_student_{}_view".format(settings.STUDENT_ID))
		rows = cursor.fetchall()
		return render(request,"logdapp/viewgrades.html",{'data':rows})
	except:
		return render(request,"logdapp/error.html")

def update_grades(request):
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
	api.subscribe("logstream")

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
			cursor = connection.cursor()
			sqlquery = "UPDATE logdapp_prof_{}_view SET Grade = '{}' WHERE Student_ID_id={} AND Course_ID_id='{}'".format(settings.PROF_ID,Grade,Rollnumber,Course)
			cursor.execute(sqlquery)
			hexquery = "".join("{:02x}".format(ord(c)) for c in sqlquery)
			api.publish("logstream", "1" ,hexquery)
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
