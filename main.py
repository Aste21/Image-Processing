from PIL import Image, ImageOps
from time import *


def single_treshold(image_f, pixels_f, treshold_f):
    for i in range(image_f.size[0]):
        for j in range(image_f.size[1]):
            arithmetic_pixel_average = (pixels_f[i, j][0] + pixels_f[i, j][1] + pixels_f[i, j][2]) / 3
            if arithmetic_pixel_average >= treshold_f:
                pixels_f[i, j] = (0, 0, 0)
            else:
                pixels_f[i, j] = (255, 255, 255)
    image_f.show()


def double_treshold(image_f, pixels_f, lower_treshold_f, upper_treshold_f):
    for i in range(image_f.size[0]):
        for j in range(image_f.size[1]):
            arithmetic_pixel_average = (pixels_f[i, j][0] + pixels_f[i, j][1] + pixels_f[i, j][2]) / 3
            if lower_treshold_f <= arithmetic_pixel_average <= upper_treshold_f:
                pixels_f[i, j] = (0, 0, 0)
            else:
                pixels_f[i, j] = (255, 255, 255)
    image_f.show()


def number_of_apperances_creator(pix_im, gray_im):
    pix_app = [0] * 256
    for x in range(gray_im.size[0]):
        for y in range(gray_im.size[1]):
            pix_app[pix_im[x, y]] += 1
    return pix_app


def cdf_creator(pix_app):
    cdf_f = [0]*256
    last_pixel = 0
    for i in range(256):
        if pix_app[i] != 0:
            cdf_f[i] = last_pixel + pix_app[i]
            last_pixel = cdf_f[i]
    return cdf_f


def cdf_min_creator(cdf_f):
    for i in range(256):
        if cdf_f[i] != 0:
            return cdf_f[i]


def histogram_creator(cdf_f, cdf_min_f, num_of_pixels, num_of_gray_levels_used):
    histogram_f = [-1]*256
    for i in range(256):
        if cdf_f[i] != 0:
            histogram_f[i] = round(((cdf_f[i] - cdf_min_f)/(num_of_pixels - cdf_min_f))*(num_of_gray_levels_used-1))
    return histogram_f


def histogram_im_creator(histogram_f, pix_values_f, size_x, size_y, original_image):
    for i in range(size_x):
        for j in range(size_y):
            pix_values_f[i, j] = histogram_f[pix_values_f[i, j]]
    original_image.show()


def average_of_rect(arr, corner_a_x, corner_a_y, corner_b_x, corner_b_y):
    sum_of_squares = 0
    num_of_squares = 0
    for i in range(corner_a_x, corner_b_x+1):
        for j in range(corner_a_y, corner_b_y+1):
            sum_of_squares += arr[i, j]
            num_of_squares += 1
    return round(sum_of_squares/num_of_squares)


def mean_filter_naive(pix_f, im_f, mask_size):
    start = time()
    temp_arr = [[0 for x in range(im_f.size[1])] for y in range(im_f.size[0])]
    for i in range(im_f.size[0]):
        for j in range(im_f.size[1]):
            half_of_mask_size = mask_size // 2
            corner_a_x = i - half_of_mask_size
            if corner_a_x < 0:
                corner_a_x = 0
            corner_a_y = j - half_of_mask_size
            if corner_a_y < 0:
                corner_a_y = 0
            corner_b_x = i + half_of_mask_size
            if corner_b_x >= im_f.size[0]:
                corner_b_x = im_f.size[0] - 1
            corner_b_y = j + half_of_mask_size
            if corner_b_y >= im_f.size[1]:
                corner_b_y = im_f.size[1] - 1
            temp_arr[i][j] = average_of_rect(pix_f, corner_a_x, corner_a_y, corner_b_x, corner_b_y)
    end = time()
    for i in range(im_f.size[0]):
        for j in range(im_f.size[1]):
            pix_f[i, j] = temp_arr[i][j]
    print(f"TIME OF NAIVE APPROACH: {end-start}")
    im_f.show()


def creating_temp_arr(im_f, pix_f):
    temp_arr = [[0 for x in range(im.size[1])] for y in range(im.size[0])]

    for i in range(im_f.size[1]):
        temp_arr[0][i] = pix_f[0, i]

    # Do column wise sum
    for i in range(1, im_f.size[0]):
        for j in range(im_f.size[1]):
            temp_arr[i][j] = pix_f[i, j] + temp_arr[i - 1][j]

    # Do row wise sum
    for i in range(im_f.size[0]):
        for j in range(1, im_f.size[1]):
            temp_arr[i][j] += temp_arr[i][j - 1]

    return temp_arr


def average_of_rect_optimized(temp_arr, corner_a_x, corner_a_y, corner_b_x, corner_b_y):
    if corner_a_x == 0 and corner_a_y == 0:
        return round(temp_arr[corner_b_x][corner_b_y]/((corner_b_x+1)*(corner_b_y+1)))
    elif corner_a_x == 0:
        return round((temp_arr[corner_a_x][corner_a_y] + temp_arr[corner_b_x][corner_b_y] - temp_arr[corner_a_x][corner_b_y] - temp_arr[corner_b_x][corner_a_y] + temp_arr[0][corner_b_y] - temp_arr[0][corner_a_y])/((corner_b_y-corner_a_y)*(corner_b_x+1)))
    elif corner_a_y == 0:
        return round((temp_arr[corner_a_x][corner_a_y] + temp_arr[corner_b_x][corner_b_y] - temp_arr[corner_a_x][
            corner_b_y] - temp_arr[corner_b_x][corner_a_y] + temp_arr[corner_b_x][0] - temp_arr[corner_a_x][0]) / (
                                 (corner_b_x - corner_a_x) * (corner_b_y + 1)))
    return round((temp_arr[corner_a_x][corner_a_y] + temp_arr[corner_b_x][corner_b_y] - temp_arr[corner_a_x][corner_b_y] - temp_arr[corner_b_x][corner_a_y])/((corner_b_x-corner_a_x)*(corner_b_y-corner_a_y)))


def mean_filter_optimized(pix_f, im_f, mask_size):
    start = time()
    temp_arr = creating_temp_arr(im_f, pix_f)

    for i in range(im_f.size[0]):
        for j in range(im_f.size[1]):
            half_of_mask_size = mask_size//2
            corner_a_x = i-half_of_mask_size-1
            if corner_a_x < 0:
                corner_a_x = 0
            corner_a_y = j - half_of_mask_size-1
            if corner_a_y < 0:
                corner_a_y = 0
            corner_b_x = i+half_of_mask_size
            if corner_b_x >= im_f.size[0]:
                corner_b_x = im_f.size[0]-1
            corner_b_y = j + half_of_mask_size
            if corner_b_y >= im_f.size[1]:
                corner_b_y = im_f.size[1] - 1
            pix_f[i, j] = average_of_rect_optimized(temp_arr, corner_a_x, corner_a_y, corner_b_x, corner_b_y)
    end = time()
    print(f"TIME OF OPTIMIZED APPROACH: {end-start}")
    im_f.show()


possible_inputs = [1, 2, 3, 4]
print("TELL ME WHAT YOU NEED!")
print("PRESS 1 FOR SINGLE TRESHOLD")
print("PRESS 2 FOR DOUBLE TRESHOLD")
print("PRESS 3 FOR EXERCISE 3")
print("PRESS 4 FOR EXERCISE 4")

a = 100


while a not in possible_inputs:
    a = input()
    if a.isdigit():
        a = int(a)
    if a not in possible_inputs:
        print("Wrong input! - Input again...")

match a:
    case 1:
        im = Image.open("yoda.jpeg")
        pix = im.load()
        treshold_1 = int(input("Input treshold: "))
        single_treshold(im, pix, treshold_1)
    case 2:
        im = Image.open("yoda.jpeg")
        pix = im.load()
        treshold_1 = int(input("Input first treshold: "))
        treshold_2 = int(input("Input second treshold: "))
        double_treshold(im, pix, treshold_1, treshold_2)
    case 3:
        im = Image.open("yoda.jpeg")
        pix = im.load()
        gray_im = ImageOps.grayscale(im)
        gray_im.show()
        pix_gray = gray_im.load()
        pix_num_app = number_of_apperances_creator(pix_gray, gray_im)
        cdf = cdf_creator(pix_num_app)
        cdf_min = cdf_min_creator(cdf)
        histogram = histogram_creator(cdf, cdf_min, gray_im.size[0]*gray_im.size[1], 256)
        histogram_im_creator(histogram, pix_gray, gray_im.size[0], gray_im.size[1], gray_im)
    case 4:
        im = Image.open("road.jpg")
        im_2 = im
        gray_im = ImageOps.grayscale(im)
        pix_gray = gray_im.load()
        gray_im.show()
        mean_filter_optimized(pix_gray, gray_im, 71)
        gray_im_2 = ImageOps.grayscale(im_2)
        pix_gray_2 = gray_im_2.load()
        mean_filter_naive(pix_gray_2, gray_im_2, 71)

