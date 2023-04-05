import math


class Region:
    def __init__(self):
        self.__points = []
        self.__edges = []
        self.__dict_points = {}
        self.__normalized = False
        self.__rect = [0, 0, 0, 0]  # x, y, width, height
        self.__center = [0, 0]
        self.__extremes = [0, 0, 0, 0]  # [min_X, max_X, min_Y, max_Y]

    def normalize(self):
        if self.__normalized:
            return
        min_X, max_X, min_Y, max_Y = [10000000, -10000000, 10000000, -10000000]
        for point in self.__points:
            x, y = point
            top_point = not self.is_inside((x - 1, y))
            bottom_point = not self.is_inside((x + 1, y))
            left_point = not self.is_inside((x, y - 1))
            right_point = not self.is_inside((x, y + 1))
            if top_point or bottom_point or left_point or right_point:
                self.__edges.append(point)
            # update extremes
            if x < min_X:
                min_X = x
            if x > max_X:
                max_X = x
            if y < min_Y:
                min_Y = y
            if y > max_Y:
                max_Y = y

        self.__extremes = [min_X, max_X, min_Y, max_Y]
        self.__center = [int((min_X + max_X) / 2), int((min_Y + max_Y) / 2)]
        self.__rect = [min_X, min_Y, max_X - min_X + 1, max_Y - min_Y + 1]
        self.__normalized = True

    def get_extremes(self):
        self.normalize()
        return self.__extremes

    def get_center(self):
        self.normalize()
        return self.__center

    def get_rect(self):
        self.normalize()
        return self.__rect

    def add_point(self, point):
        if self.is_inside(point):
            return
        self.__points.append(point)
        self.__dict_points[self.key(point)] = True

    def add_points(self, points):
        for point in points:
            self.add_point(point)

    def add_region(self, region):
        points = region.get_points()
        self.add_points(points)

    def add_regions(self, regions):
        for region in regions:
            self.add_region(region)

    def empty(self):
        return len(self.__points) == 0

    def is_inside(self, point):
        return self.key(point) in self.__dict_points

    def get_points(self):
        return self.__points

    def get_edges(self):
        return self.__edges

    def get_acreage(self):
        return len(self.__points)

    def is_all_inside(self, points):
        for point in points:
            if not self.is_inside(point):
                return False
        return True

    def is_inside_region(self, region):
        self.normalize()
        for edge in self.get_edges():
            x, y = edge
            neighbor_points = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
            outside_region_points = [
                p for p in neighbor_points if not self.is_inside(p)]
            if not region.is_all_inside(outside_region_points):
                return False
        return True

    def get_rect_extremes(self):
        self.normalize()
        min_X, max_X, min_Y, max_Y = self.__extremes
        top_left = (min_X, min_Y)
        top_right = (min_X, max_Y)
        bottom_left = (max_X, min_Y)
        bottom_right = (max_X, max_Y)
        return top_left, top_right, bottom_left, bottom_right

    def get_rect_size(self):
        self.normalize()
        min_X, max_X, min_Y, max_Y = self.__extremes
        width = max_X - min_X + 1
        height = max_Y - min_Y + 1
        return width, height

    def get_point_rate(self):
        rect_width, rect_height = self.get_rect_size()
        rect_acreage = rect_width * rect_height
        return self.get_acreage() / rect_acreage

    def is_inside_rect(self, rect):
        top_left, top_right, bottom_left, bottom_right = self.get_rect_extremes()
        return \
            Region.point_in_rect(top_left, rect) and \
            Region.point_in_rect(top_right, rect) and \
            Region.point_in_rect(bottom_left, rect) and \
            Region.point_in_rect(bottom_right, rect)

    def is_normalized(self):
        return self.__normalized

    def center_distance(self, region):
        self.normalize()
        region.normalize()
        return math.dist(self.get_center(), region.get_center())

    @staticmethod
    def key(point):
        return '|'.join(str(e) for e in point)

    @staticmethod
    def merge_two_region(region1, region2):
        points = region1.get_points() + region2.get_points()
        merge_region = Region()
        merge_region.add_points(points)
        merge_region.normalize()
        return merge_region

    @staticmethod
    def point_in_rect(point, rect):
        px, py = point
        rx, ry, rw, rh = rect
        in_range_X = px >= rx and px <= rx + rw
        in_range_Y = py >= ry and py <= ry + rh
        return in_range_X and in_range_Y
