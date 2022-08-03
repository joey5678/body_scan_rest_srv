import websocket
import time
import json 

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("$$$$$$close@@@@@")

def on_open(ws):
    ws.send('{"device_id": "123456"}')


if __name__ == "__main__":
    # ws = websocket.WebSocketApp("wss://122.51.149.232:5000/websocket",
    #                           on_message = on_message,
    #                           on_error = on_error,
    #                           on_close = on_close)
    # ws.on_open = on_open
    # ws.send("testtttt")
    # ws.run_forever()
    from websocket import create_connection
#建立WS连接
    ws = create_connection("ws://122.51.149.232:9001")
    print("Receiving...")
    result =  ws.recv()

#发送设备标识信息
    print("Sending Connect message")
    ws.send('{"type": "connect", "data": {"dev_id":"ftsk_100001"}}')
    # print("Receiving...")
    # result =  ws.recv()
    # print("Received '%s'" % result)

#等待启动扫描命令
    while True:
        print("waiting launch message")
        result =  ws.recv()
        print("Received '%s'" % result)
        json_msg = json.loads(result)
        if json_msg['type'] == 'request_launch':
            print("received launch command, start to run..")

            break
        time.sleep(10)
    # 执行3D扫描，生成obj文件并上传到云
    #After run the device to scan to generate obj file and upload to cloud, return obj file path.

# 返回obj文件云存储的路径
    print("Sending result message")
    ws.send('{"type": "return_launch", "data": {"dev_id":"123456", "obj_file_path": "https://3dp-1302477916.cos.ap-mumbai.myqcloud.com/obj/2022-07-29/1659082295053.obj"}}')
    print("Receiving...")
    result =  ws.recv()
    print("Received '%s'" % result)


    ws.close()