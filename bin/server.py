from websocket_server import WebsocketServer
import json

client_query = {}
dev_param = 'dev_id'
websrv_param = 'websrv'
websrv_client_id = -1
websrv_client = None
# Called for every client connecting (after handshake)
def new_client(client, server):
	print("New client connected and was given id %d" % client['id'])
	client_query[client['id']] = {
		'obj': client,
		'status' : 'new',
		'data': None,
		'id': -1
	}
	_cid = client['id']
	server.send_message(client, '{"type": "new_client", "data":{"_id":%d}}' % _cid)


# Called for every client disconnecting
def client_left(client, server):
	if client is not None:
		client_query.pop(client['id'], '')
		print("Client(%d) disconnected" % client['id'])
	print(client_query)

def _get_client_obj(_id):
	max_id = 0
	for _cid, _v in client_query.items():
		if _v['id'] == _id:
			if _cid > max_id:
				max_id = _cid
	if max_id > 0:
		return client_query[max_id]

	return None


# Called when a client sends a message
def message_received(client, server, message):
	global websrv_client_id
	global websrv_client
	client_query[client['id']]['data'] = message
	print("Client(%d) said: %s" % (client['id'], message))
	try:
		j_msg = json.loads(message)
	except:
		server.send_message(client, '{"type":"resp_error", "data":{"error_msg":"wrong message format, not a json string."}}')
		return
	print(f"message: {j_msg}")
	_type, _data = j_msg['type'], j_msg['data']
	cli_id = None
	is_srv = False
	if _type == 'connect':
		if _data.get(dev_param, None) is not None:
			cli_id = _data[dev_param]
		elif _data.get(websrv_param, None) is not None:
			cli_id = _data[websrv_param]
			is_srv = True
		else:
			server.send_message(client, '{"type":"resp_error", "data":{"error_msg":"data not invalid."}}')
			return
		client_query[client['id']]['id'] = cli_id #identify by this.
		client_query[client['id']]['status'] = 'connected'
		if is_srv:
			websrv_client_id = client['id']
			websrv_client = client
		server.send_message(client, '{"type":"resp_connect", "data":{"msg":"connect received."}}')
		#server.send_message(client, '{"type":"request_launch", "data":{"dev_id":"123456"}}')
	elif _type == 'request_launch':
		if client['id'] != websrv_client_id:
			server.send_message(client, '{"type":"resp_error", "data":{"error_msg":"client id not match, should be websrv id."}}')
			print(f"Server send message to {client['id']}")
			return
		if client_query[websrv_client_id]['status'] == "waiting":
			print("web client already in waiting status. abort this request or reset previous request.")
                        #return
		if _data.get(dev_param, None) is None:
			server.send_message(client, '{"type":"resp_error", "data":{"error_msg":"should contain device id in data."}}')
			print(f"Server send message to {client['id']}")
			return
		_dev_id = _data[dev_param]
		to_client = _get_client_obj(_dev_id)
		if to_client is not None:
			server.send_message(to_client, message)
			print(f"Server send message1 to {to_client['id']}")
			server.send_message(client, '{"type":"resp_req_launch", "data":{"msg":"request_launch received."}}')
			if client_query[websrv_client_id]['status'] != 'waiting':
				print(f"Server send message2 to {client['id']}")
				client_query[websrv_client_id]['status'] = 'waiting'
		else:
			server.send_message(client, '{"type":"resp_req_launch_error", "data":{"msg":f"not found device client with dev id: %d." % _dev_id}}')
			print(f"Server send message to {client['id']}")
	elif _type == 'return_launch':
		if _data.get('obj_file_path', None) is None:
			server.send_message(client, '{"type":"resp_error", "data":{"error_msg":"not found obj file path (obj_file_path) in data."}}')
			print(f"Server send message to {client['id']}")
			return
		client_query[client['id']]['status'] = 'ok'
		server.send_message(websrv_client, message)
		client_query[websrv_client_id]['status'] = 'ok'
		print(f"Server send message1 to {websrv_client['id']}")
		server.send_message(client, '{"type":"resp_ret_launch", "data":{"msg":"return_launch received."}}')
		print(f"Server send message to {client['id']}")




PORT=9001
server = WebsocketServer(host='0.0.0.0', port = PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
