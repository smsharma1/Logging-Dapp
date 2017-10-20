#!/usr/bin/python
import urllib.parse
import requests
from sys import stdin
import json

def send_data(data):
    querydata = { 'key': data}
    payload = urllib.parse.urlencode(querydata)
    url = "http://localhost:8080"

    response = requests.request("POST", url, data=payload, verify=False)
    print(response)

data = stdin.read()
data = json.loads(data);
print(data[0])

send_data(data[0])
