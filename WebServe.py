import os
import socket
import sys
import threading
import json

# 客户端类
class _Client:
    def __init__(self, _client: socket.socket, _ip):
        self.socket = _client
        self.ip = _ip
        self.name = None

    def send(self, _id, _data):
        _dict = {'id': _id,
                 'data': _data}
        _json = json.dumps(_dict)

        self.socket.send(_json.encode())


# 服务端命令函数
def _command():
    print("\n------贪吃蛇服务器------\n-----输入/h获取命令-----\n")

    while True:
        command = input()

        if command == '/h':
            print('\n----Command List----')
            print('/h:打印命令列表\n'
                  '/e:退出服务\n'
                  '/p:玩家列表\n'
                  '/c:清屏')
            print('----    end     ----\n')
            continue

        if command == '/e':
            print('\n------Closing-------')
            print('正在关闭服务...')
            snakeServer.close()
            print('已退出')
            print('----    end     ----\n')
            return

        if command == '/p':
            print('\n---- PlayerList ----')
            print('---name---ip&port---')

            for i in ccList:
                print(f'  {i.name}   {i.ip}')

            print('----    end     ----\n')
            continue

        if command == '/c':
            os.system('cls')
            continue

        print('\n----CommandError----')
        print('未知命令,输入/h获取命令列表')
        print('--------end---------\n')


# 广播消息
def sendAll(data):
    print('\n-------sendAll------')
    print(json.loads(data.decode()))
    for i in ccList:
        try:
            i.socket.send(data)
        except:
            print(f'{i.name} {i.ip} 发送失败')
            continue
    print('--------end---------\n')


# 接收数据
def receive(cc: _Client):
    global ccList
    while True:
        try:
            data = cc.socket.recv(1024)
            if len(data) == 0:
                raise Exception
        except Exception as e:
            out('close', f'{cc.name}{cc.ip} 连接关闭')

            if cc in ccList:
                ccList.pop(ccList.index(cc))
                sendAll(json.dumps({'id': 4, 'data': [cc.name]}).encode())
            break

        msgDict = json.loads(data.decode())
        out('MsgData', f'{cc.name}:{msgDict}')
        # 处理客户端传递的消息
        if msgDict['id'] == 1:
            cc.name = msgDict['data']
            sendAll(data)
            continue

        if msgDict['id'] == 2:
            sendAll(data)
            continue

        if msgDict['id'] == 3:
            sendAll(data)
            continue

        if msgDict['id'] == 4:
            ccList.pop(ccList.index(cc))
            sendAll(data)
            continue

        if msgDict['id'] == 5:
            pData = {'id': 5, 'data': [i.name for i in ccList]}
            json_pData = json.dumps(pData)
            try:
                cc.socket.send(json_pData.encode())
            except:
                out('Send Error', f'target = {cc.name} {cc.ip}\nmsgData={json_pData}')
                continue
            continue


# 格式输出
def out(msgType, msgData):
    lenT = len(msgType)
    if lenT > 20:
        print(msgType)
    else:
        len1 = int((20 - lenT) / 2)
        len2 = 20 - len1 - lenT
        msg = '\n' + '-' * len1 + msgType + '-' * len2
        print(msg)

    print(msgData)
    print('--------end---------\n')


# 变量定义
ccList = []

# 创建服务端套接字
snakeServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 设置端口号复用
snakeServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
# 监听本机25565端口
snakeServer.bind(('', 25565))
# 监听上限
snakeServer.listen(128)


# 开启命令线程
subCommand = threading.Thread(target=_command, name='command')
subCommand.setDaemon(True)
subCommand.start()

# 循环等待客户端连接
print('\n等待连接')

while True:
    try:
        client, ip = snakeServer.accept()
    except Exception as e:
        print(e)
        sys.exit(1)
    out('connect', f' {ip}连接至服务器')
    if len(ccList) == 4:
        client.close()
        continue
    # 创建_Client类
    clientClass = _Client(client, ip)
    # 加入列表
    ccList.append(clientClass)
    # 开启等待客户端发送消息子线程
    subClient = threading.Thread(target=receive, args=(clientClass,),name=str(ip))
    subClient.setDaemon(True)
    subClient.start()
