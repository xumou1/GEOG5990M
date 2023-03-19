# import packages
import random

class Agent():
    def __init__(self, i, environment, n_rows, n_cols):
        self.i = i
        self.environment = environment
        tnc = int(n_cols / 3)
        self.x = random.randint(tnc - 1, (2 * tnc) - 1)
        tnr = int(n_rows / 3)
        self.y = random.randint(tnr - 1, (2 * tnr) - 1)
        self.store = 0
    
    def __str__(self) -> str:
        return self.__class__.__name__ + "(i = " + str(self.i) + ", x = " + str(self.x) + ", y = " + str(self.y) + ")"
    
    def __repr__(self) -> str:
        return str(self)
    
    def move(self, xmin, xmax, ymin, ymax):
        if self.x < xmin:
            self.x = xmin
        if self.y < ymin:
            self.y = ymin
        if self.x > xmax:
            self.x = xmax
        if self.y > ymax:
            self.y = ymax
        else:
            if self.x >= (xmax + xmin)/2:
                self.x -= 1
            else:
                self.x += 1
    
    def eat(self):
        if self.environment[self.y][self.x] >= 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
        else:
            self.store += self.environment[self.y][self.x]
            self.environment[self.y][self.x] = 0
