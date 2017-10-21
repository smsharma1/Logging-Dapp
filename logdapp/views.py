# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from .forms import NameForm, GradeForm
from django.shortcuts import render
from Savoir import Savoir
import json
from django.conf import settings
from django.db import connection

rpcuser = 'multichainrpc'
rpcpasswd = 'BWVjg5eJJgvJbgNQL9iaoHBwLLapx369ZeWxRZHVhWAR'
rpchost = 'localhost'
rpcport = '2662'
chainname = 'demo'

api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)

@login_required(login_url="login/")
def index(request):
    return render(request,"logdapp/index.html")

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