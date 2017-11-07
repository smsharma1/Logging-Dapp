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
import json, configparser, os, binascii, base64, codecs

def index(request):
	return render(request,'logdapp/index.html')

@csrf_exempt
def grant_permissions(request):
	serverchain = settings.CHAIN_NAME
	chain_info = get_multichain_info()
	api = Savoir(chain_info["username"], chain_info["password"], "localhost", chain_info["port"], serverchain)
	if request.method == 'POST':
		data = json.loads((request.body).decode('utf-8'))
		key = data["key"]
		user = data["user"]
		password = data["password"]
		publickey = data["publickey"]
		try:
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM logdapp_user where ID_id='{}' and password='{}'".format(user,password))
			rows = cursor.fetchall()
			if rows is not None:
				api.grant(str(key), "send")
				api.grant(str(key), "logstream.write")
				cursor.execute("INSERT into logdapp_user_publickey (publickey,prof_id_id,address) values ('{}', {}, '{}')".format(publickey,user,key))
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
		print(student_data)
		digest_data = SHA256.new(student_data.encode())
		# fetch data from multichain
		serverchain = settings.CHAIN_NAME
		chain_info = get_multichain_info()
		api = Savoir(chain_info["username"], chain_info["password"], "localhost", chain_info["port"], serverchain)
		# check hash for equality
		key_alldata = api.liststreamkeyitems("logstream", key)
		cursor.execute("SELECT publickey,address FROM logdapp_user_publickey where prof_id_id = {}".format(one_row[2]))
		prof_publickeys = cursor.fetchall()
		print("prof keys data fetched from sql : ", prof_publickeys)
		publickey = RSA.importKey(prof_publickeys[0][0])
		address = prof_publickeys[0][1]
		i = 0
		for i in range(len(key_alldata)):
			recent_data = key_alldata[-1-i]
			print(recent_data['data'])						
			flag = 0
			print(publickey)			
			if( address == recent_data['publishers'][0]):
				h = binascii.unhexlify(codecs.encode(recent_data['data']))
				try:
					print("hash: ",h," digest_data: ", digest_data)
					pkcs1_15.new(publickey).verify(digest_data,h)
					flag = 1
					break
				except:
					pass
				break #because sql data needs to match with last professor's update
			else:
				#raise alarm
				pass

		if(flag == 0):
			return HttpResponse("Validation failed for {}. Talk to your instructor and OARS admin immediately.".format(one_row))

	return render(request,"logdapp/viewgrades.html",{'data':rows})
	# except:
	# 	return render(request,"logdapp/error.html")
@csrf_exempt
def blockchain_breach(request):
	if request.method == 'POST':
		data = json.loads((request.body).decode('utf-8'))
		print("Someone is making changes in bloack-chain. Look at the reverse data index {} in Logstream with key {}".format(data["rev_index"],data["key"]))
		return HttpResponse("OK")
	return HttpResponse("Default")

def update_grades(request):
	clientchain = settings.CHAIN_NAME
	chain_info = get_multichain_info()
	api = Savoir(chain_info["username"], chain_info["password"], "localhost", chain_info["port"], clientchain)
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
			encrypted_student_data = pkcs1_15.new(selfprivatekey).sign(digest_data)
			sqlquery = "UPDATE logdapp_prof_{}_view SET Grade = '{}' WHERE Student_ID_id={} AND Course_ID_id='{}'".format(settings.PROF_ID,Grade,Rollnumber,Course)				
			hexquery = codecs.decode(binascii.hexlify(encrypted_student_data))
			api.publish("logstream", key ,hexquery)
			cursor.execute(sqlquery)
			cursor.execute("SELECT * FROM logdapp_prof_{}_view".format(settings.PROF_ID))					
			rows = cursor.fetchall()
			return render(request,"logdapp/update_grades.html",{'data':rows,'form':form_class})
		except:
			 return render(request,"logdapp/error.html")
	elif request.method == 'GET':
		try:
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM logdapp_prof_{}_view".format(settings.PROF_ID))
			rows = cursor.fetchall()
			return render(request,"logdapp/update_grades.html",{'data':rows,'form':form_class})
		except:
			return render(request,"logdapp/error.html")