import threading
from json import dumps, loads
from GameWindow import Game_Win
from socket import socket
from tkinter.messagebox import showerror, showinfo
from threading import Thread
from SnakeClass import player, Snake
from time import sleep, time
from GameLogic import _Control

# 变量定义
win = Game_Win()
client = socket()
control = _Control(win.canvas)
pList = []
isConnected = False
snake = Snake(15, 15)
food = [20, 15]
multiSnake = [Snake(2, 2), Snake(5, 28), Snake(10, 10), Snake(2, 20)]
foodList = [[1, 1], [17, 19], [26, 27], [1, 19]]
directions = [[1, 0], [1, 0], [1, 0], [1, 0]]


# 函数定义
def connect(_client: socket):
    global isConnected
    if isConnected:
        return

    name = win.roomEntry.get()
    address = win.addressEntry.get()
    data1 = dumps({'id': 1, 'data': name})

    try:
        ip = (address.split(":", 1)[0], int(address.split(":", 1)[1]))
    except:
        showerror('贪吃蛇', '服务器地址有误')
        return
    if name == 'Name':
        showerror('贪吃蛇', '你还没有改名字')
        return
    try:
        _client.connect(ip)
        _client.send(data1.encode())
    except Exception as e:
        print(e)
        showerror('贪吃蛇', '连接服务器失败')
        return
    showinfo('', 'connected')
    isConnected = True
    _client.send(dumps({'id': 5, 'data': []}).encode())
    data = client.recv(1024)

    msgDict = loads(data.decode())
    for o, i in enumerate(msgDict['data']):
        p = player()
        p.order = o
        p.name = i
        pList.append(p)
    print(pList)


def recv():
    global pList, isConnected, directions
    while not isConnected:
        sleep(1)

    win.connectBtn.config(text='已连接')
    win.roomEntry.config(state='disabled')
    win.addressEntry.config(state='disabled')

    while True:
        try:
            data = client.recv(1024)
            if len(data) <= 0:
                raise ConnectionError
        except:
            isConnected = False
            print('recv error')
            break

        msgDict = loads(data.decode())

        print('msg: ',data)

        if msgDict['id'] == 1:
            client.send(dumps({'id': 5, 'data': []}).encode())
        if msgDict['id'] == 2:
            print('移动消息:', msgDict['data'])
            for i in pList:
                if i.name == msgDict['data'][0]:
                    directions[i.order] = msgDict['data'][1]
            continue

        if msgDict['id'] == 3:
            startBool = True
            print('准备消息:', msgDict['data'])
            for i in pList:
                if i.name == msgDict['data'][0]:
                    i.readyState = True
                    break

            for i in pList:
                if not i.readyState:
                    startBool = False

            if startBool:
                threading.Thread(target=multiGame, daemon=True, name='multiGame').start()
            continue

        if msgDict['id'] == 4:
            print('离开消息:', msgDict['data'])
            for i in pList:
                if i.name == msgDict['data'][0]:
                    pList.pop(i.order)

            continue

        if msgDict['id'] == 5:
            print('玩家列表消息:', msgDict['data'])
            pList = []
            for o, i in enumerate(msgDict['data']):

                p = player()
                p.order = o
                p.name = i
                pList.append(p)
                print(pList)
            continue
    win.connectBtn.config(text='连接')
    win.roomEntry.config(state='normal')
    win.addressEntry.config(state='normal')
    client.close()


def move_Control(event):
    key = event.keycode
    if key == 87 or key == 38:
        # print("'up'")
        win.direction = (0, -1)
        if isConnected:
            moveData = {'id': 2, 'data': [win.roomEntry.get(), win.direction]}
            try:
                moveData = dumps(moveData).encode('utf-8')
                client.send(moveData)
            except:
                print("向服务器传递消息失败")

    if key == 83 or key == 40:
        # print('down')
        win.direction = (0, 1)
        if isConnected:
            moveData = {'id': 2, 'data': [win.roomEntry.get(), win.direction]}
            try:
                moveData = dumps(moveData).encode('utf-8')
                client.send(moveData)
            except:
                print("向服务器传递消息失败")

    if key == 65 or key == 37:
        # print('left')
        win.direction = (-1, 0)
        if isConnected:
            moveData = {'id': 2, 'data': [win.roomEntry.get(), win.direction]}
            try:
                moveData = dumps(moveData).encode('utf-8')
                client.send(moveData)
            except:
                print("向服务器传递消息失败")

    if key == 68 or key == 39:
        # print('right')
        win.direction = (1, 0)
        if isConnected:
            moveData = {'id': 2, 'data': [win.roomEntry.get(), win.direction]}
            try:
                moveData = dumps(moveData).encode('utf-8')
                client.send(moveData)
            except:
                print("向服务器传递消息失败")


def singleGame():
    control.ResetAll()
    win.scoreNumLbl.config(text='000')
    win.gameStateLbl.config(text='游戏中')

    snake.snake = snake.orginSnake
    win.startBtn.config(state='disabled')
    control.InitSingleGame(snake.snake, food)
    snake.food = food
    while True:
        st = time()

        snake.direction = win.direction

        snake.move()

        control.moveObject(1, [snake.snake], snake.direction)

        if list(snake.food) == list(snake.snake[0]):
            snake.newFood()
            snake.snake.append(snake.snake[-1])
            win.canvas.coords(control.singleId[900],
                              snake.food[0] * 20, snake.food[1] * 20,
                              snake.food[0] * 20 + 20, snake.food[1] * 20 + 20)
            win.canvas.update()

            # calculate score
            s = int(win.scoreNumLbl.cget('text'))
            l = len(snake.snake)

            if l <= 50:
                s += 1
            if 50 < l <= 500:
                s += 2
            if l > 500:
                s += 3
            s = str(s)
            if len(s) < 3:
                s = '0' * (3 - len(s)) + s

            win.scoreNumLbl.config(text=s)

        if snake.in_wall or snake.eat_self:
            break

        sleep(0.1)
    win.gameStateLbl.config(text='游戏结束')
    win.startBtn.config(state='normal')


def multiGame():
    control.ResetAll()
    # win.resetMG(pList)

    for i in pList:
        i.gameState = True

    for i in multiSnake:
        i.snake = i.orginSnake

    control.InitMultiGame([multiSnake[i.order].snake for i in pList], [[15, 15]])

    while True:

        for i in pList:
            if i.gameState:
                multiSnake[i.order].direction = directions[i.order]
                multiSnake[i.order].move()
                control.moveObject(2, [multiSnake[i.order].snake for i in pList], directions[:len(pList)])

        sleep(0.5)


def preMultiGame():
    name = win.roomEntry.get()
    if not isConnected:
        showinfo('贪吃蛇', '未连接服务器')
        return
    if name != pList[0].name:
        print('name: ', name, 'plist[0]:', pList[0].name)
        try:
            client.send(dumps({'id': 3, 'data': [name]}).encode())
            win.multiStartBtn.config(text='已准备', state='disabled')
        except:
            showerror('贪吃蛇', '发送消息失败。\n连接丢失！')
        return

    for i in pList[1:]:
        if not i.readyState:
            showinfo('贪吃蛇', '有人未准备')
            return
    try:
        client.send(dumps({'id': 3, 'data': [name]}).encode())
    except:
        showerror('贪吃蛇', '开始失败。\n连接丢失！')
        return


Thread(target=recv, daemon=True, name='recv').start()

control.CreateSingleGameObject()
control.CreateMultiGameObject(
    colors=[['green', 'lightGreen'], ['blue', "lightSkyBlue"], ['red', 'pink'], ['cyan', 'lightCyan']])

win.connectBtnBind(lambda: Thread(target=connect, args=(client,), name='connect', daemon=True).start())
win.startBtnBind(lambda: Thread(target=singleGame, name='SingleGame', daemon=True).start())
win.multiGStartBtnBind(lambda: Thread(target=preMultiGame, name='PreMultiGame', daemon=True).start())
win.root.bind('<Key>', move_Control)

win.mainloop()
