# import packages
import random
import geometry

class Agent():
    def __init__(self, agents, i, environment, n_rows, n_cols):
        '''
        :param agents:
        :param i:
        :param environment:
        :param n_rows:
        :param n_cols:
        '''
        self.agents = agents
        self.i = i
        self.environment = environment
        tnc = int(n_cols / 3)
        self.x = random.randint(tnc - 1, (2 * tnc) - 1)
        tnr = int(n_rows / 3)
        self.y = random.randint(tnr - 1, (2 * tnr) - 1)
        self.store = random.randint(0, 99)
        self.store_shares = 0
    
    def __str__(self) -> str:
        return self.__class__.__name__ + "(i = " + str(self.i) + ", x = " + str(self.x) + ", y = " + str(self.y) + ")"
    
    def __repr__(self) -> str:
        return str(self)
    
    def move(self, xmin, xmax, ymin, ymax):
        rn = random.random()
        if rn < 0.5:
            self.x = self.x + 1
        else:
            self.x = self.x - 1
        if self.x < xmin:
            self.x = xmin
        elif self.x > xmax:
            self.x = xmax
        
        rn = random.random()
        if rn < 0.5:
            self.y = self.y + 1
        else:
            self.y = self.y - 1
        if self.y < ymin:
            self.y = ymin
        elif self.y > ymax:
            self.y = ymax
    
    def eat(self):
        if self.environment[self.y][self.x] >= 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
        else:
            self.store += self.environment[self.y][self.x]
            self.environment[self.y][self.x] = 0

        if self.store > 100:
            self.store = self.store / 2
            self.environment[self.y][self.x] = self.environment[self.y][self.x] + self.store

    def share(self, neighbourhood):
        # Create a list of agents in neighbourhood
        neighbours = []
        for agent in self.agents:
            distance = geometry.get_distance(agent.x, agent.y, self.x, self.y)
            if distance < neighbourhood:
                neighbours.append(agent.i)

        n_neighbours = len(neighbours)
        shares = self.store / n_neighbours

        for i in neighbours:
            self.agents[i].store_shares += shares
