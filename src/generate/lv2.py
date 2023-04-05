from generate.untils import *
from setup.constrants import *
import cv2


def replace_image_change(image, rectangle, location):
    location_x, location_y = location
    height = rectangle.shape[0]
    width = rectangle.shape[1]
    # print(start_x, start_y, range_x, range_y)
    for x in range(location_x, location_x + height):
        for y in range(location_y, location_y + width):
            image[x][y] = rectangle[x - location_x][y - location_y]
    return image


def lv2_generate(image_opencv, num_location):
    shape = image_opencv.shape
    width, height = shape[1], shape[0]
    locations = random_generate(TOTAL_POINTS, width - MAX_RANDOM_DISTANCE, height - MAX_RANDOM_DISTANCE, num_location)
    image_copy = image_opencv.copy()

    diff_rects = []

    for i in range(num_location):
        x, y = locations[i]
        range_width = random.randint(MIN_RANDOM_DISTANCE, MAX_RANDOM_DISTANCE)
        range_height = random.randint(MIN_RANDOM_DISTANCE, MAX_RANDOM_DISTANCE)

        diff_rects.append((x, y, range_width, range_height))

        image_change_range = image_copy[y:y+range_height, x:x+range_width]

        direct = random.randint(0, 2)
        image_change_range = cv2.flip(image_change_range, direct)

        image_copy = replace_image_change(image_copy, image_change_range, (y, x))

    #  Loại bỏ các thay đổi không đủ tiêu chuẩn
    diff_rects_remove = []
    total_diff = 0
    for  rect in diff_rects:
        total_diff = 0
        x, y, r_w, r_h = rect
        check = image_opencv[y:y+r_h, x:x+r_w] - image_copy[y:y+r_h, x:x+r_w]
        total_diff = sum(abs(check[i][j][k]) for i in range(r_h) for j in range(r_w) for k in range(0,3))
        if (total_diff < MIN_DIFFERENT * 10):
            diff_rects_remove.append(rect)
    for i in diff_rects_remove:
        diff_rects.remove(i)

    return image_copy, diff_rects
