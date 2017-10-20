# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from .forms import NameForm
from django.shortcuts import render
from Savoir import Savoir
import json

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