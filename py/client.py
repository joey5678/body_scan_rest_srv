# import the standard JSON parser
import sys
import time
import json
# import the REST library
#from restful_lib import Connection
import urllib3
import requests


urllib3.disable_warnings()

base_url = "https://api.3dmu.prototechsolutions.com/v3/models"
mock_url = "http://localhost:8888"
#mock_url = "http://122.51.149.232/api"
#base_url = mock_url
HEADERS = {'x-api-key':'EZtaDPvJDjkrEcohrkiMHYGWTimmszKJ', 'Content-Type':'application/json; charset=utf8'}


def rest_get(resource, args={}, headers=HEADERS):
    path = base_url + '/' + resource
    headers['User-Agent'] = 'Basic Agent'
    
    resp = requests.get(path, params=args, headers=headers, verify = False)
    print(resp.headers['Content-Type'])
    assert 'application/json' in resp.headers['Content-Type'], "Expect json-format response for RESTful request."
    
    status = resp.status_code

    if status == 200:
        print('Get method from 3th, return successful status code: ', status)
        print(resp.headers)
    else:
        print('Get method from 3th,abnormal status code: ', status)
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


if __name__ == "__main__":
    #args = {"requestId" : "ff490320-94b1-11ec-9522-4f5e1b8d858c"}
    #args = {"requestId" : "4d086260-976c-11ec-b671-d9134b5d86fc"}
    #args = {"requestId" : "bf13e7c0-9bc8-11ec-93ba-b5564ac072f9"}
    
    #_, rsp = rest_get("metrics", args) 
    #print(rsp)
    cos_path = 'https://3dp-1302477916.cos.ap-mumbai.myqcloud.com/test'
    body_json = {
        "type": "all",
        "fileurl": f"{cos_path}/xleg.obj",
        "orientation_matrix": "1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1",
        "filesource": "url",
        "filetype": "obj",
        "output": "json"
        }

    print("POS")
    scode, rsp = rest_post("measure", body=body_json)
    print(rsp)
    if scode != 200:
        sys.exit(-1)
    req_id = rsp['requestId']
    time.sleep(10)    
    print("GET")
    args = {"requestId" : req_id}
    _, rsp_g = rest_get("metrics", args) 
    print(rsp_g)
