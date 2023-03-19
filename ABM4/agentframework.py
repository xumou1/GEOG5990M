# import packages
import random

class Agent():
    def __init__(self, i) -> None:
        self.i = i
        self.x = random.randint(0, 99)
        self.y = random.randint(0, 99)
    
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