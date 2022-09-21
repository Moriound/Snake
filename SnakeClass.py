import random
import time


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.snake = [(x, y), (x - 1, y)]
        self.direction = (1, 0)
        self.snakeId = []
        self.food = (-1, -1)
        self.lastDirection = self.snake[-1]

    def move(self):
        self.lastDirection = self.snake[-1]

        for i in range(self.len):
            if i != self.len - 1:
                self.snake[self.len - i - 1] = self.snake[self.len - i - 2]
        self.snake[0] = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

    @property
    def len(self):
        return len(self.snake)

    @property
    def head(self):
        return self.snake[0]

    def eat_food(self):
        if self.food in self.snake:
            return True
        else:
            return False

    @property
    def eat_self(self):
        if self.snake[0] in self.snake[1:]:
            return True
        else:
            return False

    @property
    def in_wall(self):
        if self.snake[0][0] > 29 or self.snake[0][0] < 0 or self.snake[0][1] > 29 or self.snake[0][1] < 0:
            return True
        else:
            return False

    @property
    def orginSnake(self):
        return [(self.x, self.y), (self.x - 1, self.y)]

    def newFood(self):
        self.food = [random.randint(1, 28), random.randint(1, 28)]


class player:
    def __init__(self):
        self.name = None
        self.order = None
        self.readyState = False
        self.snake = None
        self.gameState = False  # false 不在游戏 true 游戏中
        self.score = 0

    def __repr__(self):
        return f'<name={self.name},' \
               f'order={self.order},' \
               f'readyState={self.readyState},' \
               f'snake={self.snake},' \
               f'gameState={self.gameState},' \
               f'score={self.score}>'

# if __name__ == '__main__':
#     x = Snake(15, 15)
#     c = Snake(3, 0)
#     print('x ', x.moveR)
#     print('c', c.moveR)
#     x.direction = (0, 1)
#     x.food=(15,16)
#     c.move()
#     x.move()
#     print('x', x.moveR)
#     print('c', c.moveR)
#
#     c.move()
#     x.move()
#     print('x', x.moveR)
#     print('c', c.moveR)
#
#     print(x.eat_food())
#     print(x.moveR)
