import requests
import json
import os

ENDPOINT = "http://127.0.0.1:8000/jwt/"
R_ENDPOINT = ENDPOINT + "refresh/"
AUTH_ENDPOINT = "http://127.0.0.1:8000/user/profile/auth/"
headers = {
    "Content-Type" : "application/json",
}

data = {
    'email': 'minhaj',
    'password': '12345'
}

r = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)
token = r.json()['token']

print(token)

headers = {
    "Content-Type" : "application/json",
    "Authorization": "JWT "+ token
}
ref_req = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)

print(ref_req.json())