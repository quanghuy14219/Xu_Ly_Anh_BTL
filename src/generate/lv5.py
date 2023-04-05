from generate.untils import *
from setup.constrants import *
import cv2


def replace_image_change(origin_img, range_r, start_pos):
    start_x, start_y = start_pos
    range_x = range_r.shape[0]
    range_y = range_r.shape[1]
    # print(start_x, start_y, range_x, range_y)
    for x in range(start_x, start_x + range_x):
        for y in range(start_y, start_y + range_y):
            origin_img[x][y] = range_r[x - start_x][y - start_y]
    return origin_img


def lv5_generate(opencv_img, num_range):
    shape = opencv_img.shape
    width, height = shape[1], shape[0]
    g_img = opencv_img.copy()
    diff_rects = []

    icop = cv2.Canny(g_img, 50, 150, 30)
    # g_img = replace_range(g_img, icop, (width, height))

    return icop, diff_rects
