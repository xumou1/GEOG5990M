import math

def get_distance(x0, y0, x1, y1):
    distance = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    return distance


def get_max_distance(agents):
    max_distance = 0
    for i in range(len(agents)):
        for j in range(i + 1, len(agents)):
            distance = get_distance(agents[i].x, agents[i].y, agents[j].x, agents[j].y)
            max_distance = max(distance, max_distance)

    return max_distance


def get_min_distance(agents):
    min_distance = math.inf
    for i in range(len(agents)):
        for j in range(i + 1, len(agents)):
            distance = get_distance(agents[i].x, agents[i].y, agents[j].x, agents[j].y)
            min_distance = min(distance, min_distance)

    return min_distance


def get_min_max_distance(agents):
    min_distance = math.inf
    max_distance = 0
    for i in range(len(agents)):
        for j in range(i + 1, len(agents)):
            distance = get_distance(agents[i].x, agents[i].y, agents[j].x, agents[j].y)
            min_distance = min(distance, min_distance)
            max_distance = max(distance, max_distance)

    return (max_distance, min_distance)