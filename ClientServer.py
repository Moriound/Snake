import json
import socket
import threading
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('218.89.171.149', 62872))


def recv(_client: socket.socket):
    while True:
        try:
            data = _client.recv(1024)
            if len(data) == 0:
                print('data.len = 0')
                _client.close()
                break
        except:
            print('recv error')
            break
        msgDict = json.loads(data.decode())

        if msgDict['id'] == 2:
            print('移动消息:', msgDict['data'])
            continue

        if msgDict['id'] == 3:
            print('准备消息:', msgDict['data'])
            continue

        if msgDict['id'] == 4:
            print('离开消息:', msgDict['data'])
            continue

        if msgDict['id'] == 5:
            print('玩家列表消息:', msgDict['data'])
            continue


subRecv = threading.Thread(target=recv, args=(client,),name='recv')
subRecv.setDaemon(True)
subRecv.start()

name = input('name:')

while True:
    _id = int(input('id:'))
    msg = [
        json.dumps({'id': 1, 'data': name}).encode('utf-8'),
        json.dumps({'id': 2, 'data': [name, (1, 0)]}).encode('utf-8'),
        json.dumps({'id': 3, 'data': [name, '已准备']}).encode('utf-8'),
        json.dumps({'id': 4, 'data': [name]}).encode('utf-8'),
        json.dumps({'id': 5, 'data': []}).encode('utf-8'),
    ]
    client.send(msg[_id - 1])
