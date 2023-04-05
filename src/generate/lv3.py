from generate.untils import *
from setup.constrants import *
import cv2
import numpy as np


def replace_image_change(origin_img, range_r, start_pos):
    start_x, start_y = start_pos
    range_x = range_r.shape[0]
    range_y = range_r.shape[1]
    # print(start_x, start_y, range_x, range_y)
    for x in range(start_x, start_x + range_x):
        for y in range(start_y, start_y + range_y):
            origin_img[x][y] = range_r[x - start_x][y - start_y]
    return origin_img


def lv3_generate(image_opencv, num_location):
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

        # Canny(ảnh, giá trị ngưỡng trên, giá trị ngưỡng dưới, kích thước kernel)
        canny_image = cv2.Canny(image_change_range, 50, 150, 30)

        # Xác định giá trị màu trung bình
        tmp = (0, 0, 0)
        count = 0
        for xi in range(0, range_height): 
            for yi in range(0, range_width):
                if canny_image[xi][yi] != 255:
                    tmp += image_change_range[xi][yi]
                    count += 1
        tmp = tmp / count
        
        # Biến đổi các điểm ảnh
        for xi in range(1, range_height-1): 
            for yi in range(1, range_width-1):
                # Nếu đây là một điểm trong cạnh thì
                if canny_image[xi][yi] == 255:
                    # Thay đổi giá trị của điểm
                    val = (tmp*6 + image_change_range[xi][yi])/7
                    image_change_range[xi][yi] = val

                    # Làm mịn ảnh
                    kernel = cv2.getGaussianKernel(5, 0)
                    kernel = np.outer(kernel, kernel.transpose())
                    image_change_range[xi-1:xi+2, yi-1:yi+2] = cv2.filter2D(image_change_range[xi-1:xi+2, yi-1:yi+2], -1, kernel)

        image_copy = replace_image_change(image_copy, image_change_range, (y, x))

    #  Loại bỏ các thay đổi không đủ tiêu chuẩn
    diff_rects_remove = []
    total_diff = 0
    for  rect in diff_rects:
        total_diff = 0
        x, y, r_w, r_h = rect
        check = image_opencv[y:y+r_h, x:x+r_w] - image_copy[y:y+r_h, x:x+r_w]
        total_diff = sum(abs(check[i][j][k]) for i in range(r_h) for j in range(r_w) for k in range(0,3))
        if (total_diff < MIN_DIFFERENT):
            diff_rects_remove.append(rect)
    for i in diff_rects_remove:
        diff_rects.remove(i)
    return image_copy, diff_rects
