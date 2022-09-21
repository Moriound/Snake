import random
import time
import tkinter
import threading

win = tkinter.Tk()
food = ()
snake = [(15, 15), [14, 15]]
movexy = (1, 0)
t = []

win.title("贪吃蛇")
win.geometry("800x600+400+200")
win.resizable(0, 0)

ca = tkinter.Canvas(win, width=600, height=600, bg='white')
btn = tkinter.Button(text='开始游戏', padx=10, pady=10)
lab1 = tkinter.Label(text='长度', width=4, height=1, font=("宋体", 16, "bold"), bg='lightgreen', padx=10, pady=10)
lab2 = tkinter.Label(text='', width=3, height=1, font=("宋体", 16, "normal"), bg='lightgreen', padx=10, pady=10)
lab3 = tkinter.Label(text='', font=("宋体", 32, "normal"), padx=10, pady=10)
# lab4 = tkinter.Label(text='',padx=10,pady=10)


ca.place(x=0, y=0)
btn.place(x=660, y=50)
lab1.place(x=620, y=300)
lab2.place(x=700, y=300)
lab3.place(x=640, y=120)


def draw(ca: tkinter.Canvas, x, y, color):
    ca.create_rectangle(x * 20, y * 20, x * 20 + 20, y * 20 + 20, fill=color, outline='white')


def init_ui(ca: tkinter.Canvas):
    global food, snake
    food = (random.randint(0, 29), random.randint(0, 29))
    while food in snake:
        food = (random.randint(0, 30), random.randint(0, 30))
    draw(ca, food[0], food[1], "purple")

    snake = [(15, 15), [14, 15]]
    lab2.config(text='2')
    lab3.config(text='')
    for i in snake:
        if snake.index(i) != 0:
            draw(ca, i[0], i[1], "lightgreen")
        else:
            draw(ca, i[0], i[1], "green")


def move_direction(event):
    global movexy
    key = event.keycode
    # print(key)
    if key == 87 or key == 38:
        # print("'up'")
        movexy = (0, -1)

    if key == 83 or key == 40:
        # print('down')
        movexy = (0, 1)

    if key == 65 or key == 37:
        # print('left')
        movexy = (-1, 0)

    if key == 68 or key == 39:
        # print('right')
        movexy = (1, 0)


def die():
    btn.config(state='normal')
    lab3.config(text='Game\nOver')


def move(ca: tkinter.Canvas):
    global snake
    global food
    last_direction = snake[-1]
    len_snake = len(snake)
    for i in range(len_snake):
        if i != len_snake - 1:
            snake[len(snake) - i - 1] = snake[len_snake - i - 2]
    snake[0] = (snake[0][0] + movexy[0], snake[0][1] + movexy[1])

    draw(ca, snake[0][0], snake[0][1], "green")
    draw(ca, snake[1][0], snake[1][1], "lightgreen")

    draw(ca, last_direction[0], last_direction[1], 'white')

    # 判断蛇，食物，墙的关系
    if food in snake:
        snake.append(last_direction)
        draw(ca, last_direction[0], last_direction[1], 'lightgreen')
        food = (random.randint(0, 29), random.randint(0, 29))
        draw(ca, food[0], food[1], "purple")
        lab2.config(text=str(len(snake)))

    if snake[0] in snake[1:]:
        return 'end'

    head = snake[0]
    if head[0] < 0 or head[0] > 29 or head[1] < 0 or head[1] > 29:
        return 'end'


def start(*args):
    global t

    ca.create_rectangle(0, 0, 650, 650, fill='white', outline='white')
    init_ui(ca)  # 初始化画布

    time.sleep(0.5)
    while True:
        s_t = int(time.time() * 1000)
        res = move(ca)
        if res == 'end':
            die()
            break
        e_t = int(time.time() * 1000)
        d_t = 0.18 - float(e_t - s_t) / 1000.0
        if d_t > 0:
            time.sleep(d_t)
        if len(snake) == 900:
            break
    return


def click_start(*args):
    s = threading.Thread(target=start)
    s.start()
    btn.config(state='disabled')


btn.config(command=click_start)
win.bind('<Key>', move_direction)

win.mainloop()


"""
    version 1.1：
        更换监听键盘方式，由pynput改为tkinter event
    version 1.2:
        更换开始游戏按钮的绑定方式，由bind()改为command
"""