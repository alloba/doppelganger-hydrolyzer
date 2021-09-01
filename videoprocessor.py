import cv2
import numpy as np
from multiprocessing import Pool, Process
import multiprocessing
import os


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
    write_string = 'source,r,g,b\n'
    for nested_list in color_avg_array:
        write_string += tgt_file.split('/')[-1].split('.')[0] + ', ' + ', '.join(map(str, nested_list)) + '\n'
    with open(tgt_file, 'w') as f:
        f.write(write_string)


# Extract data points from all files in the target folder.
# Should attempt to skip processing for data that already exists to save time in case of edited data / paused execution
def process_video_pointmaps(image_file_list, output_directory):
    print('processing pointmaps... ')
    pool = Pool(multiprocessing.cpu_count() - 2)
    for index, file_path in enumerate(image_file_list):
        pool.apply_async(process_video_pointmap, args=(file_path, output_directory, index+1, len(image_file_list)+1))
    pool.close()
    pool.join()
    print('\ndone')


def process_video_pointmap(image_file, output_directory, position=None, total=None):
    print(f'{position}/{total} video processing', end='\r')
    target_file = output_directory + image_file.split('/')[-1].split('.')[0] + '.txt'

    if os.path.isfile(target_file):
        return

    color_average = calculate_video_averages(image_file)
    save_video_data(color_average, target_file)


def collate_pointmaps(source_files, target_directory):
    print('collating pointmaps... ')
    f = open(target_directory + '/collated-pointmap.csv', 'w')
    f.write('')
    f.close()

    with open(target_directory + '/collated-pointmap.csv', 'a') as out_file:
        output = 'source,r,g,b\n'
        out_file.write(output)
        for file in source_files:
            with open(file) as tst_file:  # current implementation has a lot of video processing errors that manifest as zero data points in output files.
                if len(tst_file.readlines()) < 2:
                    continue
            with open(file) as csvfile:
                for row in csvfile.readlines()[1:]:
                    out_file.write(row)
    print('done')


def load_pointmap(file):
    with open(file) as tst_file:  # current implementation has a lot of video processing errors that manifest as zero data points in output files.
        if len(tst_file.readlines()) < 2:
            return [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

    with open(file) as csvfile:
        output = []
        for row in csvfile.readlines()[1:]:
            vals = [float(vals.strip()) for vals in row.split(",")[1:]]
            output.append(vals)

        return output
