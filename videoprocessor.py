import cv2
import numpy as np


def get_average_color(image):
    # https://www.timpoulsen.com/2018/finding-the-dominant-colors-of-an-image.html
    height, width, _ = np.shape(image)

    # calculate the average color of each row of our image
    avg_color_per_row = np.average(image, axis=0)

    # calculate the averages of our rows
    avg_colors = np.average(avg_color_per_row, axis=0)

    # avg_color is a tuple in BGR order of the average colors
    # but as float values
    return avg_colors


def calculate_video_averages(file):
    capture = cv2.VideoCapture(file)
    try:
        frame_number = 0
        averages = []
        while capture.isOpened():
            frame_number += 1
            ret, frame_image = capture.read()
            if ret is False:
                break
            average_rgb = get_average_color(frame_image)
            averages.append(average_rgb.tolist())
        return averages
    finally:
        capture.release()
        cv2.destroyAllWindows()


def save_video_data(color_avg_array, tgt_file):
    write_string = ''
    for nested_list in color_avg_array:
        write_string += ', '.join(map(str, nested_list)) + '\n'
    with open(tgt_file, 'w') as f:
        f.write(write_string)

    print(f'\t{len(color_avg_array)} data points.')
