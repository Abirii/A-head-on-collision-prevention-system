'''
Finding Lane Lines on the Road functions:
convert_HSL_colorspace() - convert RGB image to HSL colorspace, more details about HSL can be found in http://www.chaospro.de/documentation/html/paletteeditor/colorspace_hsl.htm
convert_gray_scale() - Convert image to gray scale.
detect_white_and_yellow() - Detect yellow and white colors --> http://colorizer.org/
smoothing() - Smooth out rough edges and return smooth image.
ROI() - Exclude outside the region of interest.
create_mask() - Create maks for ROI.
detection() - Get Image from car thread.
crop_left() - Crop the left side,Check if there is lanes in our left.
crop_right() - Crop the right side,Check if there is lanes in our right.
count_lanes() - Get left or right side of the image and count the number of lines.
determine_side() - Determine the side of the car
'''

import cv2 as cv
import numpy as np
import process as proc

# Convert RGB image to HSL colorspace, and return the image.
# The HSL color space defines colors more naturally,(Hue,Saturation,Lightness),return HLS!!
# For more detailshttp://www.chaospro.de/documentation/html/paletteeditor/colorspace_hsl.htm and http://hslpicker.com/#fff
def convert_HSL_colorspace(image):
    HSL_image = cv.cvtColor(image,cv.COLOR_RGB2HLS)
    proc.save_to_procedure('HSL.jpg', HSL_image)
    return HSL_image

# Detect yellow and white colors --> http://colorizer.org/
def detect_white_and_yellow(image):
    # Convert to HSL colorspace.
    HSL_image = convert_HSL_colorspace(image)

    # White mask.
    lower = np.uint8([0, 200, 0])
    upper = np.uint8([255, 255, 255])
    white_mask = cv.inRange(HSL_image,lower,upper)
    proc.save_to_procedure('white_mask.jpg',white_mask)
    mask =  cv.bitwise_and(image,image,mask = white_mask)
    proc.save_to_procedure('bitwise_and.jpg',mask)

    return mask

# Convert image to gray scale
def convert_gray_scale(image):
    gray_image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    proc.save_to_procedure('gray.jpg', gray_image)
    return gray_image

# Smooth out rough edges
def smoothing(image):
    kernel_size = 9
    smooth_image = cv.GaussianBlur(image,(kernel_size,kernel_size),0)
    proc.save_to_procedure('smooth_image.jpg',smooth_image)
    return smooth_image

# Edges detection
def detect_edges(image):
    lower_threshold = 150 # If a pixel gradient value is below the lower threshold, then it is rejected.
    upper_threshold = 300 # If a pixel gradient is higher than the upper threshold, the pixel is accepted as an edge.
    # Else is between, then it will be accepted only if it is connected to a pixel that is above the upper threshold.
    edges = cv.Canny(image,lower_threshold,upper_threshold)
    proc.save_to_procedure('detect_edges.jpg',edges)
    return edges

# Create maks for ROI and get lanes
def create_ROI(image):

    points = define_points_ROI(image)
    mask = np.zeros_like(image)
    cv.fillPoly(mask,points,255)
    proc.save_to_procedure('ROI_mask.jpg',mask)
    lane = cv.bitwise_and(image,mask)
    proc.save_to_procedure('lane_only.jpg',lane)
    return lane

# Define points for ROI
def define_points_ROI(image):
    rows = image.shape[0]
    cols = image.shape[1]

    bottom_left = [cols * 0.01, rows * 0.95]
    top_left = [cols * 0.3, rows * 0.5]
    bottom_right = [cols, rows * 0.95]
    top_right = [cols * 0.7, rows * 0.5]

    points =  np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
    return points


# Determine the side of the car return True for pass, else False
def determine_side(image):

   left = crop_left(image)
   right = crop_right(image)
   # The lane line on our left
   if left >= 1:
       return 0

   # The lane line on our right
   elif right >= 1:
       return 1

# Check if there is lanes in out left
def crop_left(image):
    height, width = image.shape[:2]
    # Crop 0.4 from image for left side
    start_row, start_col = int(0), int(0)
    end_row, end_col = int(height), int(width * .4)

    cropped_left = image[start_row:end_row, start_col:end_col]
    cropped_left = cv.resize(cropped_left,(int(width),int(height)))
    # Number of lines on left
    left_lanes = count_lanes(cropped_left)

    return left_lanes


# Check if there is lanes in our right
def crop_right(image):
    height, width = image.shape[:2]
    # Crop 0.6 from image for right side
    start_row, start_col = int(0), int(width * .5)
    end_row, end_col = int(height), int(width)

    cropped_right = image[start_row:end_row, start_col:end_col]
    cv.resize(cropped_right, (int(width), int(height)))
    # Number of lines on right
    right_lanes = count_lanes(cropped_right)

    return right_lanes

# Get left or right side of the image and count the number of lines.
def count_lanes(image):
    # Grab all the contours
    contours, hierarchy = cv.findContours(image,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    counter = 0

    for cnt in contours:
        counter += 1

    return counter


# Get Image from car thread, return True for pass
def detection(car_input):
        proc.save_to_procedure('Input.jpg',car_input)
        mask = detect_white_and_yellow(car_input)
        gray_image = convert_gray_scale(mask)
        smooth_image = smoothing(gray_image)
        edges = detect_edges(smooth_image)
        lane_image = create_ROI(edges)
        out_of_lane = determine_side(lane_image)

        return out_of_lane
