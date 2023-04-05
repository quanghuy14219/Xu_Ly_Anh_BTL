import random
import numpy as np
from setup.constrants import *


def rand_poses(max_x, max_y, count):
    rands = []
    for i in range(count):
        x = random.randint(1, max_x)
        y = random.randint(1, max_y)
        rands.append((x, y))
    return rands


def square_distance(point1, point2):
    return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2


def rally_distance(point, rally, dis_calc=square_distance):
    distances = [dis_calc(point, ral) for ral in rally]
    return min(distances)


def rally_max_distance(cur_rally, choose_rally):
    distances = [rally_distance(point, cur_rally) for point in choose_rally]
    max_index = np.argmax(distances)
    point_max = choose_rally[max_index]
    return point_max, distances[max_index], max_index


def random_generate(max_random, max_x, max_y, num_choose, start_index=0):
    choose_rally = rand_poses(max_x, max_y, max_random)
    cur_rally = [choose_rally[start_index]]
    del choose_rally[start_index]
    for i in range(num_choose):
        point, distance, index = rally_max_distance(cur_rally, choose_rally)
        # print(distance)
        cur_rally.append(point)
        del choose_rally[index]
    return cur_rally


def rand_color():
    x1 = random.randint(0, 256)
    x2 = random.randint(0, 256)
    x3 = random.randint(0, 256)
    return x1, x2, x3
