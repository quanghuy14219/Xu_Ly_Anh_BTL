from skimage.metrics import structural_similarity as ssim
from setup.constrants import *
import imutils
import cv2


def get_new_size(max_width, max_height, img_width, img_height):
    scale = 1
    if img_width > img_height:
        scale = max_width/img_width
    else:
        scale = max_height/img_height

    new_width = int(img_width * scale)
    new_height = int(img_height * scale)

    return new_width, new_height


def calc_ssim(img1, img2, rect):
    x, y, w, h = rect
    rect1 = img1[y:y+h, x:x+w]
    rect2 = img2[y:y+h, x:x+w]
    gray1 = cv2.cvtColor(rect1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(rect2, cv2.COLOR_BGR2GRAY)
    score, diff = ssim(gray1, gray2, full=True)
    diff = (diff * 255).astype("uint8")
    return score, diff


class SSIM_Detecter:
    def __init__(self, image1, image2, max_width=600, max_height=400) -> None:
        self.img1 = image1
        self.img2 = image2
        self.max_width = max_width
        self.max_height = max_height
        self.differents = self.get_differents()

    def get_size(self):
        shape = self.img1.shape
        return shape[1], shape[0]

    def get_differents(self):
        cur_size = self.get_size()
        new_size = get_new_size(
            self.max_width, self.max_height, cur_size[0], cur_size[1])
        self.img1 = cv2.resize(self.img1, new_size)
        self.img2 = cv2.resize(self.img2, new_size)

        gray1 = cv2.cvtColor(self.img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(self.img2, cv2.COLOR_BGR2GRAY)

        # Compute SSIM between two images
        score, diff = ssim(gray1, gray2, full=True)
        diff = (diff * 255).astype("uint8")

        # print("SSIM: {}".format(score))

        # Threshold the difference image
        thresh = cv2.threshold(
            diff, 10, 200, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        
        # Find contours to get regions of two input images that different
        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        differents = []
        # Loop over the contours
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            rect_area = w * h
            if rect_area > 100:
                differents.append((x, y, w, h))
        return differents

    def get_SSIM(self):
        ssimes = []
        for rect in self.differents:
            x, y, w, h = rect
            rect1 = self.img1[y:y+h, x:x+w]
            rect2 = self.img2[y:y+h, x:x+w]
            gray1 = cv2.cvtColor(rect1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(rect2, cv2.COLOR_BGR2GRAY)
            score, diff = ssim(gray1, gray2, full=True)
            diff = (diff * 255).astype("uint8")
            ssimes.append((score, diff))
        return ssimes


class SubtractDetecter:
    def __init__(self, opencv_img1, opencv_img2, max_width=600, max_height=400) -> None:
        self.img1 = opencv_img1
        self.img2 = opencv_img2
        self.max_width = max_width
        self.max_height = max_height
        self.differents = self.get_differents()

    def get_size(self):
        shape = self.img1.shape
        return shape[1], shape[0]

    def get_differents(self):
        cur_size = self.get_size()
        new_size = get_new_size(
            self.max_width, self.max_height, cur_size[0], cur_size[1])
        self.img1 = cv2.resize(self.img1, new_size)
        self.img2 = cv2.resize(self.img2, new_size)

        # sub_img = self.img1
        # black_img = self.img2

        sub_img = self.img1 - self.img2
        black_img = self.img2 - self.img1

        self.ssim_detecter = SSIM_Detecter(sub_img, black_img)
        return self.ssim_detecter.get_differents()

    def get_SSIMs(self):
        ssimes = []
        for rect in self.differents:
            score, diff = calc_ssim(self.img1, self.img2, rect)
            ssimes.append(score)
        return ssimes


if __name__ == "__main__":
    print("Run")
    calc = SSIM_Detecter("src/images/city1.jpg", "src/images/city2.jpg")
    # diff = get_different_rectangles(
    #     "src/images/city1.jpg", "src/images/city2.jpg")
    print(len(calc.get_differents()))
    print(calc.get_size())

    # print(get_new_size(600, 360, 4500, 3000))
