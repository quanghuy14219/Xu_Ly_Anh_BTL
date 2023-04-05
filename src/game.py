import pygame
from setup.constrants import *
from untils.diff_rects import *
from untils.translate import *
from generate.lv1 import *
from generate.lv2 import *
from generate.lv3 import *
from generate.lv4 import *
from components.Button import *
import cv2

# Images
# IMG1 = "src/images/i5.jpg"
# IMG1 = "src/images/d1.png"
IMG1 = "src/images/d0.png"
# IMG1 = "src/images/city1.jpg"

# Load images
img1 = cv2.imread(IMG1)
img1 = cv2.resize(img1, get_new_size(600, 400, img1.shape[1], img1.shape[0]))

# Level 1 - Tô màu
# Level 2 - Lật
# Level 3 - Đường + Gaussian (Làm mịn)
img2, differents = lv4_generate(img1, 9)


# Init detecter
detecter = SubtractDetecter(img1, img2)
differents = detecter.differents
SSIMs = detecter.get_SSIMs()
# print(SSIMs)

# size = img1.shape[:2]
IMAGE_WIDTH = img1.shape[1]
IMAGE_HEIGHT = img1.shape[0]
SCREEN_WIDTH = IMAGE_WIDTH * 2 + PADDING
SCREEN_HEIGHT = IMAGE_HEIGHT


pygame.init()
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


img1_screen = covert_opencv_img_to_pygame(img1)
img2_screen = covert_opencv_img_to_pygame(img2)

def print_all_differents():
    for dif in differents:
        trans_rect = get_transform_range(
            dif, IMAGE_WIDTH, PADDING)
        pygame.draw.rect(screen, COLOR_RED,
                         pygame.Rect(dif),  2)
        pygame.draw.rect(screen, COLOR_RED,
                         pygame.Rect(trans_rect),  2)

    pygame.display.flip()


def draw_images():
    screen.blit(img1_screen, (0, 0))
    screen.blit(img2_screen, (IMAGE_WIDTH + PADDING, 0))
    pygame.display.flip()


def draw_true(range1, range2):
    pygame.draw.rect(screen, COLOR_RED,
                     pygame.Rect(range1),  2)
    pygame.draw.rect(screen, COLOR_RED,
                     pygame.Rect(range2),  2)
    pygame.display.flip()


def draw_fail(pos1, pos2):
    # Draw fail circle
    pygame.draw.circle(screen, COLOR_RED, pos1, 25, 2)
    pygame.draw.circle(screen, COLOR_RED, pos2, 25, 2)
    pygame.display.flip()


def draw_fail_ranges(fail_ranges):
    for pos, _ in fail_ranges:
        trans_pos = get_trans_pos(
            pos, IMAGE_WIDTH, PADDING)
        draw_fail(pos, trans_pos)


def draw_true_ranges(true_ranges):
    for range in true_ranges:
        trans_range = get_transform_range(
            range, IMAGE_WIDTH, PADDING)
        draw_true(range, trans_range)


#
true_ranges = []
fail_ranges = []


draw_images()
# print_all_differents()


# Timer for redraw scene
timer = pygame.time.set_timer(pygame.USEREVENT, 1000)
clock = pygame.time.Clock()

# Game status
status = {
    "Total Different": len(differents),
    "Total Fail": 0,
    "Total True": 0,
    "IsChanged": False,
    "IsPrintDifferent": False,
    "Logs": True
}

font = pygame.font.SysFont("Arial", 20)
btn_show = Button("Show", (IMAGE_WIDTH, 0), 20, feedback="Hide")
btn_clear = Button("Clear", (IMAGE_WIDTH, 50), 20, feedback="Clear")
# btn_new_game = Button("New game", (IMAGE_WIDTH, 250), 20, feedback="New game")


def draw_text(text, pos):
    text = font.render(text, 1, COLOR_WHITE)
    text_rect = text.get_rect()
    text_rect.topleft = pos
    screen.blit(text, text_rect)
    pygame.display.flip()


def draw_mid():
    pygame.draw.rect(screen, COLOR_BLACK,
                     pygame.Rect(IMAGE_WIDTH, 0, PADDING, IMAGE_HEIGHT))
    btn_show.show(screen)
    btn_clear.show(screen)
    draw_text("Total: {}".format(
        status["Total Different"]), (IMAGE_WIDTH, 100))
    draw_text("True:  {}".format(
        status["Total True"]), (IMAGE_WIDTH, 150))
    draw_text("Fail:  {}".format(
        status["Total Fail"]), (IMAGE_WIDTH, 200))
    # btn_new_game.show(screen)
    pygame.display.flip()


def btn_show_callback():
    status["IsPrintDifferent"] = not status["IsPrintDifferent"]
    status["IsChanged"] = True


def btn_clear_callback():
    status["Total True"] = 0
    status["Total Fail"] = 0
    true_ranges.clear()
    status["IsChanged"] = True

# def btn_new_game_callback():
#     img2, differents = lv1_generate(img1, 9)
#     status["IsChanged"] = True
    


draw_mid()

# Game loop
running = True
while running:
    if status["IsChanged"]:
        draw_images()
        draw_fail_ranges(fail_ranges)
        draw_true_ranges(true_ranges)
        status["IsChanged"] = False
        if status["IsPrintDifferent"]:
            print_all_differents()
        if status["Logs"]:
            print(status)
        draw_mid()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Btn event loader
        btn_show.click(event, btn_show_callback)
        btn_clear.click(event, btn_clear_callback)
        # btn_new_game.click(event, btn_new_game_callback)

        # User event to draw fail click range
        if event.type == pygame.USEREVENT:
            new_fail_ranges = [
                pos for pos, tick_time in fail_ranges if pygame.time.get_ticks() - tick_time >= 1000]
            if (len(new_fail_ranges) != len(fail_ranges)):
                fail_ranges = new_fail_ranges
                status["IsChanged"] = True

        # Event handle click event
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            origin_pos, is_click_padding = get_click_pos_origin(
                pos, IMAGE_WIDTH, PADDING)
            # Click padding
            if is_click_padding:
                continue

            trans_pos = get_trans_pos(origin_pos, IMAGE_WIDTH, PADDING)
            range_clicked = get_clicked_range(differents, origin_pos)
            if range_clicked is not None:
                ssim_score, _ = calc_ssim(
                    img1, img2, range_clicked)
                print(ssim_score)
                if not is_choosed_range(true_ranges, origin_pos):
                    true_ranges.append(range_clicked)
                    status["Total True"] += 1
                    status["IsChanged"] = True
            else:
                fail_ranges.append(
                    (origin_pos, pygame.time.get_ticks()))
                status["Total Fail"] += 1
                status["IsChanged"] = True

    clock.tick(60)

# Quit Pygame
pygame.quit()
