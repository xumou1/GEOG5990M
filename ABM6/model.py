import numpy as np
import matplotlib.pyplot as plt
import agentframework as af
import test_io as io
import geometry
import imageio
import os
import operator


def sum_environment(environment):
    return np.sum(environment)


def sum_agent_store(agents):
    sum_store = 0
    for agent in agents:
        sum_store += agent.store
    return sum_store

if __name__ == '__main__':
    environment, n_rows, n_cols = io.read_data()
    agents = []
    n_agents = 10
    for i in range(n_agents):
        # Create an agent
        agents.append(af.Agent(agents, i, environment, n_rows, n_cols))
        print(agents[i])

    n_iterations = 10
    x_min = 0
    x_max = n_cols - 1
    y_min = 0
    y_max = n_rows - 1
    neighbourhood = 100
    # For storing images
    global item_number
    item_number = 0
    images = []
    # Create directory to write images to.
    try:
        os.makedirs('C:/Users/dell/Desktop/leeds/GEOG5990M/ABM6/images/')
    except FileExistsError:
        print("path exists")

    # Model loop
    for ite in range(n_iterations):
        print("Iteration", ite)
        # Move agents
        print("Move")
        for i in range(n_agents):
            plt.scatter(agents[i].x, agents[i].y, color = 'black')
            # Plot the coordinate with the largest x red
            lx = max(agents, key=operator.attrgetter('x'))
            plt.scatter(lx.x, lx.y, color='red')
            # Plot the coordinate with the smallest x blue
            sx = min(agents, key=operator.attrgetter('x'))
            plt.scatter(sx.x, sx.y, color='blue')
            # Plot the coordinate with the largest y yellow
            ly = max(agents, key=operator.attrgetter('y'))
            plt.scatter(ly.x, ly.y, color='yellow')
            # Plot the coordinate with the smallest y green
            sy = min(agents, key=operator.attrgetter('y'))
            plt.scatter(sy.x, sy.y, color='green')
            plt.ylim(y_max / 3, y_max * 2 / 3)
            plt.xlim(x_max / 3, x_max * 2 / 3)
            plt.imshow(environment)
            filename = 'C:/Users/dell/Desktop/leeds/GEOG5990M/ABM6/images/' + str(item_number) + '.png'
            item_number = item_number + 1
            plt.savefig(filename)
            plt.show()
            plt.close()
            images.append(imageio.imread(filename))
            agents[i].move(x_min, y_min, x_max, y_max)
            agents[i].eat()
            #print(agents[i])
        # Share store
        # Distribute shares
        for i in range(n_agents):
            agents[i].share(neighbourhood)
        # Add store_shares to store and set store_shares back to zero
        for i in range(n_agents):
            print(agents[i])
            agents[i].store = agents[i].store_shares
            agents[i].store_shares = 0
        print(agents)
        # Print the maximum distance between all the agents
        print("Maximum distance between all the agents", geometry.get_max_distance(agents))
        # Print the total amount of resource
        sum_as = sum_agent_store(agents)
        print("sum_agent_stores", sum_as)
        sum_e = sum_environment(environment)
        print("sum_environment", sum_e)
        print("total resource", (sum_as + sum_e))
        # imageio.mimsave('C:/Users/dell/Desktop/leeds/GEOG5990M/ABM6/images/out.gif', images, fps=3)


