import numpy as np
import matplotlib.pyplot as plt
import cv2
from cell import Cell
from nonogram import Nonogram
import pygame
import time


WIDTH = 1000
HEIGHT = 600
cell_width = 20
FPS = 30

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (125, 125, 125)
YELLOW = (200, 200, 0)
BLACK = (0, 0, 0)

# initalize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nonogram")
clock = pygame.time.Clock()
screen.fill((0, 50, 110))

live_img = pygame.image.load("D:/Documents/Python/nonogram/images/heart.png").convert()
live_img = pygame.transform.scale(live_img, (25, 25))
live_img.set_colorkey(BLACK)

def image_normalize(image):
    count = 0
    mean = 0
    delta = 0
    delta2 = 0
    M2 = 0
    for line in image:
        for pixel in line:
            count = count + 1
            delta = pixel - mean
            mean = mean + delta / count
            delta2 = pixel - mean
            M2 = M2 + delta * delta2

    std = np.sqrt(M2 / (count - 1))
    return mean, std


def read_image(path):
    my_image = cv2.imread(path)
    my_image = np.asarray(my_image)
    gray_image = cv2.cvtColor(my_image, cv2.COLOR_BGR2GRAY)
    width = gray_image.shape[1]
    height = gray_image.shape[0]
    ratio = width / height
    if width > height:
        width = 25
        height = (1/ratio) *25
    else:
        height = 25
        width = ratio * 25
    dimensions = (int(height), int(width))
    resized_image = cv2.resize(gray_image, dimensions, interpolation=cv2.INTER_AREA)
    mean, std = image_normalize(resized_image)
    ret, th1 = cv2.threshold(resized_image, mean + std // 2, 255, cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(resized_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 45, 5)
    th3 = cv2.adaptiveThreshold(resized_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 45, 15)

    titles = ['Original Image', 'Global Thresholding (v = 127)',
                'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    images = [resized_image, th1, th2, th3]
    for i in range(4):
        plt.subplot(2, 2, i+1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()
    return th1


def initialize_cells(my_image):
    width = my_image.shape[1] * cell_width
    height = my_image.shape[0] * cell_width
    nonogram = Nonogram(width, height, cell_width)
    for i in range(cell_width, height + cell_width, cell_width):
        for j in range(cell_width, width + cell_width, cell_width):
            if my_image[(i - cell_width)//cell_width, (j - cell_width)//cell_width] == 0:
                color = BLACK
            else:
                color = WHITE
            cell = Cell(((j - cell_width)//cell_width, (i - cell_width)//cell_width), j, i, color, cell_width)
            nonogram.add_cell(cell)
    return nonogram, width, height


def draw_lives(lives):
    for i in range(lives):
        img_rect = live_img.get_rect()
        img_rect.x = width + 100 + 30 * i
        img_rect.y = 15
        screen.blit(live_img, img_rect)


def build_grid():
    # pygame.draw.rect(screen, YELLOW, (cell_width, cell_width, width, height), cell_width // 2)
    j = cell_width
    counter = 0
    for i in range(cell_width, width + 2*cell_width, cell_width):
        if counter % 5 == 0:
            pygame.draw.line(screen, GRAY, [i, j], [i, j + height], 5)
        pygame.draw.line(screen, GRAY, [i, j], [i, j + height])
        counter += 1
    i = cell_width
    counter = 0
    for j in range(cell_width, height + 2*cell_width, cell_width):
        if counter % 5 == 0:
            pygame.draw.line(screen, GRAY, [i, j], [i + width, j], 5)
        pygame.draw.line(screen, GRAY, [i, j], [i + width, j])
        counter += 1
    pygame.display.update()


path = r'D:\Documents\Python\nonogram\images\eagle_2.png'
my_image = read_image(path)
nonogram, width, height = initialize_cells(my_image)
pygame.draw.rect(screen, WHITE, (cell_width, cell_width, width, height))
# nonogram.update_screen(screen)
build_grid()
nonogram.build_numbers(screen)
lives = 3
nonogram.solver(screen, clock)

running = True
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    pygame.display.flip()
    draw_lives(lives)
    # process input (events)
    if lives == 0:
        font = pygame.font.Font('freesansbold.ttf', 48)
        text = font.render("GAME OVER", True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.center = (width // 2, height // 2)
        screen.blit(text, textRect)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            try:
                pressed = nonogram.check_cell(pos)
                if pressed.color == (0, 0, 0):
                    pressed.update_cell(screen, (0, 0, 0))
                    pressed.state = 1
                else:
                    pressed.update_cell(screen, RED)
                    time.sleep(0.5)
                    pressed.update_cell(screen, WHITE)
                    pressed.cross(screen)
                    pressed.state = 0
                    lives -= 1
                    pygame.draw.rect(screen, (0, 50, 110), (width + 100, 0, WIDTH, HEIGHT))
            except AttributeError:
                print("Out of bounds!")
                break
        elif pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            pressed = nonogram.check_cell(pos)
            try:
                print(pressed.id)
            except AttributeError:
                print("Out of bounds!")
                break
            if pressed.color == (255, 255, 255):
                pressed.cross(screen)
                pressed.state = 0
            else:
                pressed.update_cell(screen, RED)
                time.sleep(0.5)
                pressed.update_cell(screen, BLACK)
                pressed.state = 1
                lives -= 1
                pygame.draw.rect(screen, (0, 50, 110), (width + 100, 0, WIDTH, HEIGHT))

