import websocket
import time
import json 

from websocket import create_connection

def new_connect(ws=None):
    if ws is not None:
        try:
            ws.close()
        except:
            pass

    ws = create_connection("ws://122.51.149.232:9001")
    print("Receiving...")
    print(ws.recv())
    return ws

ws = new_connect()

print("Sending Connect message")
ws.send('{"type": "connect", "data": {"websrv":"1122334455"}}')
print("Receiving...")
result =  ws.recv()
print("Received '%s'" % result)

print("Sending launch request message")
ws.send('{"type": "request_launch", "data": {"dev_id":"ftsk_100001"}}')
# print("Receiving...")
# result =  ws.recv()
# print("Received '%s'" % result)

# while True:
#     print("wait")
#     result =  ws.recv()
#     print("Received '%s'" % result)
#     json_msg = json.loads(result)
#     if json_msg['type'] == 'return_launch':
#         print("received launch result, request finished.")
#         print(json_msg)
#         break
#     elif json_msg['type'] == 'resp_req_launch':
#         time.sleep(2)
#     elif "error" in json_msg['type'] :
#         print(f"receive error msg: {json_msg}. ")
#         break
#     else:
#         print(f"other msg: {json_msg}")

for i in range(5):
    ws = new_connect(ws)


ws.close()



