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
from Crypto.PublicKey import RSA
from itertools import chain
from logdapp.utils import get_multichain_info
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import json, configparser, os, binascii

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

	chain_info = get_multichain_info()
	api = Savoir(chain_info["username"], chain_info["password"], "localhost", chain_info["port"], serverchain)

	if request.method == 'POST':
		for key, value in request.POST.lists():
			print("%s %s" % (key, value))
		data = json.loads((request.body).decode('utf-8'))
		key = data["key"]
		user = data["user"]
		password = data["password"]
		publickey = data["publickey"]
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
				cursor.execute("INSERT into logdapp_user_publickey values ('{}', {})".format(str(publickey),user))
				return HttpResponse("Successfully received data")
			else:
				return HttpResponse("Incorrect Username or Password")
		except:
			return render(request,"logdapp/error.html")
	else:
		return HttpResponse("Please send a post request with key")

def get_grades(request):
	# try:
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM logdapp_student_{}_view".format(settings.STUDENT_ID))
	rows = cursor.fetchall()

	for one_row in rows:
		print(one_row)
		key = str(one_row[0]) + "," + str(one_row[1]) + "," + str(one_row[2])
		student_data = str(one_row[0]) + "," + str(one_row[1]) + "," + str(one_row[2]) + "," + str(one_row[3])
		digest_data = SHA256.new(student_data.encode())
		# fetch data from multichain
		serverchain = "chain1"
		chain_info = get_multichain_info()
		api = Savoir(chain_info["username"], chain_info["password"], "localhost", chain_info["port"], serverchain)
		# check hash for equality
		key_alldata = api.liststreamkeyitems("logstream", key)
		recent_data = key_alldata[-1]
		h = recent_data['data']
		flag = 0
		cursor.execute("SELECT publickey FROM logdapp_user_publickey where ID_id = {}".format(one_row[2]))
		prof_publickeys = cursor.fetchall()
		for publickey in prof_publickeys:
			try:
				print("hash: ",h," digest_data: ", digest_data)
				pkcs1_15.new(publickey).verify(h, digest_data)
				flag = 1
			except:
				pass
			
		if(flag == 0):
			return HttpResponse("Validation failed for {}. Talk to your instructor and OARS admin immediately.".format(one_row))

	return render(request,"logdapp/viewgrades.html",{'data':rows})
	# except:
	# 	return render(request,"logdapp/error.html")

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
	print(api.getinfo())

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
			encoded_key = open("rsa_key.bin", "rb").read()
			selfprivatekey = RSA.import_key(encoded_key, passphrase=str("temp"))
			cursor = connection.cursor()
			key = str(Course) + "," + str(Rollnumber) + "," + str(settings.PROF_ID)
			student_data = str(Course) + "," + str(Rollnumber) + "," + str(settings.PROF_ID) + "," + str(Grade)
			digest_data = SHA256.new(student_data.encode())
			print("digest_data: ", digest_data)
			encrypted_student_data = pkcs1_15.new(selfprivatekey).sign(digest_data)
			sqlquery = "UPDATE logdapp_prof_{}_view SET Grade = '{}' WHERE Student_ID_id={} AND Course_ID_id='{}'".format(settings.PROF_ID,Grade,Rollnumber,Course)				
			hexquery = "".join("{:02x}".format(ord(c)) for c in str(encrypted_student_data[0]))
			api.publish("logstream", key ,hexquery)
			cursor.execute(sqlquery)
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
