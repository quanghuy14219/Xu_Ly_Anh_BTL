import random
from setup.constrants import *
from generate.untils import *


def lv1_generate(image_opencv, num_location):
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

        #  Tìm giá trị màu để thay thế
        val = image_copy[y+range_height//2][x+range_width//2]
        max_val = max(val)
        for i in range(3):
            if val[i] == max_val:
                val[i] = max_val *15 //16
                break    

        image_copy[y:y+range_height, x:x+range_width] = val
    return image_copy, diff_rects


if __name__ == "__main__":
    print(random_generate(100, 600, 399, 8))
