import threading
import time
import tkinter
import GameWindow
import SnakeClass


class _Control:
    def __init__(self, canvas: tkinter.Canvas, ):
        self.canvas = canvas
        self.singleId = []
        self.multiId = [[], [], [], []]
        self.alive = []

    def CreateSingleGameObject(self):
        c = self.canvas
        # body
        for i in range(899):
            _id = c.create_rectangle(-20, 0, 0, -20, fill='lightGreen')
            self.singleId.insert(0, _id)
        # food
        _id = c.create_rectangle(-20, 0, 0, -20, fill='purple')
        self.singleId.append(_id)
        # head
        _id = c.create_rectangle(-20, 0, 0, -20, fill='Green')
        self.singleId.insert(0, _id)
        return self.singleId

    def InitSingleGame(self, snakePosList: list, foodPos: list):
        m = self.canvas.move
        for i in range(len(snakePosList)):
            _id = self.singleId[i]
            dx = snakePosList[i][0] * 20 + 20
            dy = snakePosList[i][1] * 20 + 20
            m(_id, dx, dy)

        _id = self.singleId[900]
        dx = foodPos[0] * 20 + 20
        dy = foodPos[1] * 20 + 20
        m(_id, dx, dy)

    def CreateMultiGameObject(self, colors=None):
        if colors is None:
            colors = [['Green', 'lightGreen']]
        c = self.canvas

        for j in range(4):
            # body
            for i in range(899):
                _id = c.create_rectangle(-20, 0, 0, -20, fill=colors[j][1])
                self.multiId[j].insert(0, _id)
            # food
            _id = c.create_rectangle(-20, 0, 0, -20, fill='purple')
            self.multiId[j].append(_id)
            # head
            _id = c.create_rectangle(-20, 0, 0, -20, fill=colors[j][0])
            self.multiId[j].insert(0, _id)
        return self.multiId

    def InitMultiGame(self, snakeList, foodList):
        """
        :param snakeList: 蛇坐标列表构成的列表
        :param foodList: 食物坐标列表
        """
        m = self.canvas.move
        num = len(snakeList)
        for j in range(num):
            for i in range(len(snakeList[j])):
                _id = self.multiId[j][i]
                dx = snakeList[j][i][0] * 20 + 20
                dy = snakeList[j][i][1] * 20 + 20
                m(_id, dx, dy)

        for num, food in enumerate(foodList):
            _id = self.multiId[num][900]
            dx = food[0] * 20 + 20
            dy = food[1] * 20 + 20
            m(_id, dx, dy)

            self.canvas.update()

    def ResetAll(self):

        coord = self.canvas.coords
        if len(self.singleId) > 0:
            for i in self.singleId:
                coord(i, -20, 0, 0, -20)
        if len(self.multiId) > 0:
            for j in range(len(self.multiId)):
                for i in self.multiId[j]:
                    coord(i, -20, 0, 0, -20)
        self.canvas.update()

    def moveObject(self, mode, snakeList, direction):
        """
        :param mode: 1(s),2(m)
        :param snakeList: 传入由蛇坐标列表的列表[snake1,snake2,...]
        :param direction:GameWindow.GameWin().direction
        """
        c = self.canvas.coords

        if mode == 1:
            _len = len(snakeList[0])

            # 移动尾巴到原头的位置
            x1, y1, x2, y2 = c(self.singleId[0])
            c(self.singleId[_len - 1], x1, y1, x2, y2)

            # 移动头
            x = direction[0]
            y = direction[1]
            self.canvas.move(self.singleId[0], x * 20, y * 20)

            # 改变ID次序
            tail = self.singleId[_len - 1]
            self.singleId.pop(_len - 1)
            self.singleId.insert(1, tail)

            # 更新画布
            self.canvas.update()
        else:
            mLen = [len(i) for i in snakeList]
            num = len(direction)

            for j in range(num):
                # 移动尾巴到原头的位置
                x1, y1, x2, y2 = c(self.multiId[j][0])
                c(self.multiId[j][mLen[j] - 1], x1, y1, x2, y2)
                # 移动头
                x = direction[j][0]
                y = direction[j][1]
                self.canvas.move(self.multiId[j][0], x * 20, y * 20)
                # 改变ID次序
                tail = self.multiId[j][mLen[j] - 1]
                self.multiId[j].pop(mLen[j] - 1)
                self.multiId[j].insert(1, tail)
                # 更新画布
                self.canvas.update()




# test content (unimportant)
if __name__ == '__main__':
    def mo():
        while True:
            st = time.time()
            d = win.direction
            for snake in multiSnake:
                snake.direction = d
                snake.move()

                if (15, 15) == snake.snake[0]:
                    snake.snake.append(snake.snake[-1])

            controler.moveObject(2, [snakek.snake for snakek in multiSnake],
                                 [snakej.direction for snakej in multiSnake])

            et = time.time()
            print(int((et - st) * 1000))
            time.sleep(0.12)


    def callMO():
        x = threading.Thread(target=mo, daemon=True, name='MoveObject')
        x.start()


    win = GameWindow.Game_Win()
    controler = _Control(win.canvas)
    multiSnake = [SnakeClass.Snake(2, 2), SnakeClass.Snake(3, 3), SnakeClass.Snake(4, 4), SnakeClass.Snake(5, 5)]

    controler.CreateMultiGameObject([['green', 'lightGreen'], ['blue', 'lightBlue'],
                                     ['red', 'pink'], ['cyan', 'lightCyan']])

    controler.InitMultiGame([snake.snake for snake in multiSnake], [[15, 15]])

    win.multiStartBtn.config(command=callMO)

    win.mainloop()
