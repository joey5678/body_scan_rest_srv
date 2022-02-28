# import the standard JSON parser
import json
# import the REST library
#from restful_lib import Connection
import urllib
import requests

base_url = "https://api.3dmu.prototechsolutions.com/v3/models"
mock_url = "http://10.240.118.91:8888"
base_url = mock_url
HEADERS = {'x-api-key':'EZtaDPvJDjkrEcohrkiMHYGWTimmszKJ'}


def rest_get(resource, args={}, headers=HEADERS):
    path = base_url + '/' + resource
    headers['User-Agent'] = 'Basic Agent'
    
    resp = requests.get(path, params=args, headers=headers)
    print(resp.headers['Content-Type'])
    assert 'application/json' in resp.headers['Content-Type'], "Expect json-format response for RESTful request."
    
    status = resp.status_code

    if status == 200:
        print(resp.headers)
    else:
        print('Error status code: ', status)
        print(resp.headers)

    return status, resp.json()

def rest_post(resource, body={}, headers=HEADERS):
    path = base_url + '/' + resource
    headers['User-Agent'] = 'Basic Agent'
    print(f"[rest_post] path is {path}, body is {body}")
    resp = requests.post(path, data=body, headers=headers)
    print(resp)
    assert 'application/json' in resp.headers['Content-Type'], "Expect json-format response for RESTful request."

    status = resp.status_code
    if status in (200, 202):
        print(resp.headers)
    else:
        print('Error status code: ', status)
        #print(resp.headers)

    return status, resp.json()


if __name__ == "__main__":
    args = {"requestId" : "ff490320-94b1-11ec-9522-4f5e1b8d858c"}
    args = {"requestId" : "4d086260-976c-11ec-b671-d9134b5d86fc"}
    _, rsp = rest_get("metrics", args) 
    print(rsp)

    body_json = {
        "type": "all",
        "fileurl": "https://3dp-1302477916.cos.ap-mumbai.myqcloud.com/test/2022-01-04_17-30-40.obj",
        "orientation_matrix": "1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1",
        "filesource": "url",
        "filetype": "obj",
        "output": "json"
        }

    print("POS")
    _, rsp = rest_post("measure", body=body_json)
    print(rsp)

