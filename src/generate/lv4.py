import numpy
import cv2
import queue
from generate.untils import *
from setup.constrants import *
from untils.region import *
import numpy as np


def check_in_range(point, max_dims):
    max_row, max_col = max_dims
    row, col = point
    return row >= 0 and row < max_row and col >= 0 and col < max_col

def growth_forest(location, dimensions, canny_image, marks, mark_value=False):
    q = queue.Queue()
    region = Region()
    max_row, max_col = dimensions

    q.put(location)
    while not q.empty():
        row, col = q.get()
        if 0 <= row < max_row and 0 <= col < max_col and marks[row][col] != mark_value:
            marks[row][col] = mark_value
            region.add_point((row, col))
            if canny_image[row][col] != WHITE:
                for drow, dcol in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                    q.put((row + drow, col + dcol))
    return region

#  Thuật toán xói mòn
def erode_edge(image_opencv, kernel=(5, 5), iterations=1):
    kernel = np.ones(kernel, np.uint8)
    erosion = cv2.erode(image_opencv, kernel, iterations)
    return erosion

# Thuật toán dãn nở
def dilate_edge(image_opencv, kernel=(5, 5), iterations=1):
    kernel = np.ones(kernel, np.uint8)
    dilation = cv2.dilate(image_opencv, kernel, iterations)
    return dilation

# Thuật toán loại bỏ các lỗ trống
def close_edge(image_opencv, kernel=(5, 5)):
    kernel = np.ones(kernel, np.uint8)
    closing = cv2.morphologyEx(image_opencv, cv2.MORPH_CLOSE, kernel)
    return closing

# Xử lý ảnh từ thuật toán Canny
def fix_canny_image(canny_image):
    image_update = dilate_edge(canny_image, kernel=(2, 2))
    image_update = close_edge(image_update, kernel=(2, 2))
    image_update = erode_edge(image_update, kernel=(2, 2))
    return image_update


def filter(region):
    point_rate = region.get_point_rate()
    acreage = region.get_acreage()
    rect_width, rect_height = region.get_rect_size()
    wh_rate = rect_width / rect_height
    if wh_rate > 1:
        wh_rate = 1 / wh_rate
    valid_point_rate = point_rate > 0.3
    valid_acreage = acreage > 300 and acreage < 20000
    valid_rect_size = rect_width > 4 and rect_height > 4
    valid_wh_rate = wh_rate > 0.3
    return valid_acreage and valid_point_rate and valid_rect_size and valid_wh_rate


def distance(region, regions):
    distances = [r.center_distance(region) for r in regions]
    return min(distances)

def max_distance(regions, chose_regions):
    distances = [distance(region, chose_regions)
                 for region in regions]
    max_index = np.argmax(distances)
    region_max = regions[max_index]
    return region_max, distances[max_index], max_index

def choose_regions(regions, num_location, start_index=0):
    if len(regions) <= num_location:
        return regions
    chose_regions = [regions[start_index]]
    del regions[start_index]
    for _ in range(num_location - 1):
        region, _, index = max_distance(
            regions, chose_regions)
        # print(distance)
        chose_regions.append(region)
        del regions[index]
    return chose_regions

def lv4_generate(image_opencv, num_location = 9):
    
    edged_img = cv2.Canny(image_opencv, 100, 200)
    edged_img = fix_canny_image(edged_img)

    regions = []
    empty_area = numpy.full(image_opencv.shape[:2], True)
    for row, col in numpy.ndindex(image_opencv.shape[:2]):
        if not empty_area[row, col]:
            continue
        region = growth_forest((row, col), image_opencv.shape[:2], edged_img, empty_area)
        if not region.empty():
            regions.append(region)

    regions = [region for region in regions if filter(region)]
    random.shuffle(regions)
    regions = choose_regions(regions, num_location)
    image_copy = image_opencv.copy()

    for region in regions:
        region.normalize()
        for point in region.get_points():
            val = image_copy[point]
            max_val = max(val)
            for i in range(3):
                if val[i] == max_val:
                    val[i] = max_val *2 //3
                    break 
            image_copy[point] = val

    print("Len:", len(regions))

    return image_copy, []