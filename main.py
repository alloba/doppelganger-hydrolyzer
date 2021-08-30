import sys
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import itertools

if __name__ != '__main__':
    print('Cannot run this program as a supporting module.')
    sys.exit(1)


def get_target_files(directory):
    dir_sanitized = directory if directory.endswith("/") else directory + '/'
    if directory is None:
        files = os.listdir('')
    else:
        files = os.listdir(directory)

    return [dir_sanitized + x for x in files if os.path.isfile(dir_sanitized + x)]


def save_target_frame(file, target_frame, out_dir):
    capture = cv2.VideoCapture(file)
    i = 0
    while capture.isOpened():
        ret, frame = capture.read()
        if ret is False or i > target_frame:
            break
        if i == target_frame:
            cv2.imwrite(out_dir + '/' + 'testout-frame' + str(target_frame) + '.jpg', frame)
        i += 1

    capture.release()
    cv2.destroyAllWindows()


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


# def plot_example():
#     fig = plt.figure()
#     ax = fig.gca(projection='3d')
#
#     # plotting the points
#     max_x = 0
#     max_y = 0
#     max_z = 0
#     for p in tst_list:
#         if max_x < p[0]:
#             max_x = p[0]
#         if max_y < p[1]:
#             max_y = p[1]
#         if max_z < p[2]:
#             max_z = p[2]
#         ax.scatter(p[0], p[1], p[2], zdir='z', c='r')
#
#     ax.legend()
#     # ax.set_xlim3d(0, 1)
#     # ax.set_ylim3d(0, 2)
#     # ax.set_zlim3d(0, 3)
#     ax.set_xlim3d(0, max_x)
#     ax.set_ylim3d(0, max_y)
#     ax.set_zlim3d(0, max_z)
#
#     plt.show()


def save_video_data(color_avg_array, target_file):
    write_string = ''
    for nested_list in color_avg_array:
        write_string += ', '.join(map(str, nested_list)) + '\n'
    with open(target_file, 'w') as f:
        f.write(write_string)

    print(f'\t{len(color_avg_array)} data points.')


TARGET_DIRECTORY = os.getcwd() + '/test-files/'

image_files = get_target_files(TARGET_DIRECTORY)

for index, file_path in enumerate(image_files):
    print(f'Processing {index + 1} of {len(image_files)} files...')
    target_file = TARGET_DIRECTORY + '/output/' + file_path.split('/')[-1] + '.txt'

    if os.path.isfile(target_file):
        print(f'\tData already exists for {file_path} in output directory -- Skipping processing.')
        continue

    color_average = calculate_video_averages(file_path)
    save_video_data(color_average, target_file)

