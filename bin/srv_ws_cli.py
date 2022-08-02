import websocket
import time
import json 

from websocket import create_connection
ws = create_connection("ws://122.51.149.232:9001")
print("Receiving...")
result =  ws.recv()

print("Sending Connect message")
ws.send('{"type": "connect", "data": {"websrv":"1122334455"}}')
print("Receiving...")
result =  ws.recv()
print("Received '%s'" % result)

print("Sending launch request message")
ws.send('{"type": "request_launch", "data": {"dev_id":"123456"}}')
print("Receiving...")
result =  ws.recv()
print("Received '%s'" % result)

while True:
    print("waiting launch result message")
    result =  ws.recv()
    print("Received '%s'" % result)
    json_msg = json.loads(result)
    if json_msg['type'] == 'return_launch':
        print("received launch result, request finished.")
        print(json_msg)
        break
    time.sleep(10)

ws.close()



