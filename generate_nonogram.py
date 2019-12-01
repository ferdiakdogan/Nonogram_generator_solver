import numpy as np
import matplotlib.pyplot as plt
import cv2
from cell import Cell
from nonogram import Nonogram


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
    print('Mean: ', mean)
    print('Std', std)
    return mean


def read_image(path):
    my_image = cv2.imread(path)
    my_image = np.asarray(my_image)
    gray_image = cv2.cvtColor(my_image, cv2.COLOR_BGR2GRAY)
    print("Original image: ", my_image.shape)
    dimensions = (int(gray_image.shape[1] * 10 / 100), int(gray_image.shape[0] * 10 / 100))
    resized_image = cv2.resize(gray_image, dimensions, interpolation=cv2.INTER_AREA)
    print("Resized Image: ", resized_image.shape)
    mean = image_normalize(resized_image)
    ret, th1 = cv2.threshold(resized_image, mean + 50, 255, cv2.THRESH_BINARY)
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


path = r'D:\Documents\Python\nonogram\images\apple.jpg'
my_image = read_image(path)
cell_width = 10
width = my_image.shape[1] * cell_width
height = my_image.shape[0] * cell_width
nonogram = Nonogram(width, height, cell_width)
