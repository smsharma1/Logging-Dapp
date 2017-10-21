#!/usr/bin/python
import urllib.parse
import requests
from sys import stdin
import json

def send_data(data):
    querydata = { 'key': str(data)}
    # payload = urllib.parse.urlencode(querydata)
    payload = json.dumps(querydata)
    url = "http://127.0.0.1:8000/logdapp/grantpermissions/"

    response = requests.request("POST", url, data=payload, verify=False)
    print(response)

data = stdin.read()
data = json.loads(data);
print(data[0])

send_data(data[0])
