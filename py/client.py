# import the standard JSON parser
import sys
import time
import json
# import the REST library
#from restful_lib import Connection
import urllib3
import requests


urllib3.disable_warnings()

base_url = "http://122.51.149.232:9900/v1/models"
HEADERS = {'Content-Type':'application/json; charset=utf8'}

def rest_get(resource, args={}, headers=HEADERS):
    path = base_url + '/' + resource
    headers['User-Agent'] = 'Basic Agent'
    
    resp = requests.get(path, params=args, headers=headers, verify = False)
    print(resp.headers['Content-Type'])
    assert 'application/json' in resp.headers['Content-Type'], "Expect json-format response for RESTful request."
    
    status = resp.status_code

    if status == 200:
        print('Get method from bgo, return successful status code: ', status)
        print(resp.headers)
    else:
        print('Get method from bgo,abnormal status code: ', status)
        print(resp.text)

    return status, resp.json()

def rest_post(resource, body={}, headers=HEADERS):
    path = base_url + '/' + resource
    headers['User-Agent'] = 'Basic Agent'
    print(f"[rest_post] path is {path}, body is {body}")
    print(type(body), body)
    resp = requests.post(path, data=json.dumps(body), headers=headers, verify = False)
    print(resp)
    assert 'application/json' in resp.headers['Content-Type'], "Expect json-format response for RESTful request."

    status = resp.status_code
    print(f"post return status code : {status}, type: {type(status)}.")
    if status in (200, 202):
        print(resp.headers)
    else:
        print('Error status code: ', status)
        #print(resp.headers)

    return status, resp.json()
