import sys
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import itertools
import videoprocessor as vp
import analytics
import csv

if __name__ != '__main__':
    print('Cannot run this program as a supporting module.')
    sys.exit(1)


def get_files_list(directory):
    dir_sanitized = directory if directory.endswith("/") else directory + '/'
    if directory is None:
        files = os.listdir('')
    else:
        files = os.listdir(directory)

    return [dir_sanitized + x for x in files if os.path.isfile(dir_sanitized + x)]


def load_pointmap(file):
    with open(file) as csvfile:
        output = []
        for row in csvfile.readlines():
            vals = [float(vals.strip()) for vals in row.split(",")]
            output.append(vals)
        return output


# Extract data points from all files in the target folder.
# Should attempt to skip processing for data that already exists to save time in case of edited data / paused execution
def process_video_pointmaps(image_file_list, output_directory):
    for index, file_path in enumerate(image_file_list):
        print(f'Processing {index + 1} of {len(image_file_list)} files...')
        target_file = output_directory + file_path.split('/')[-1].split('.')[0] + '.txt'

        if os.path.isfile(target_file):
            print(f'\tData already exists for {file_path} in output directory -- Skipping processing.')
            continue

        color_average = vp.calculate_video_averages(file_path)
        vp.save_video_data(color_average, target_file)
    print('\n')


# For all data data collections, run DTW calculations against all of them.
# Output will be stored in files with the name of the comparing file.
# Meaning, for files a,b,c there will be 3 files named a,b,c with 3 distances + filenames inside.
def process_dtw_crossover(pointmap_file_list, output_dir):
    print(f'Processing DTW values for {len(pointmap_file_list)} files...')
    print(f'Outputting results to {output_dir}')
    for i in pointmap_file_list:
        output_text = ''
        for j in pointmap_file_list:
            ii = load_pointmap(i)
            jj = load_pointmap(j)
            dist = analytics.dtw_distance_d(ii, jj)

            output_text += f'{j}, {dist}\n'
        with open(output_dir + i.split('/')[-1].split('.')[0] + '.txt', 'w') as out_file:
            out_file.write(output_text)
    print('\n')


def collate_dtw_data(dtw_files_list, output_dir):
    print('Collating results into single file...')
    output_txt = ''
    for f in dtw_files_list:
        filename = f.split('/')[-1].split('.')[0]
        ff = open(f, 'r')
        data = ff.readlines()
        for d in data:
            target_file = d.split(',')[0].strip().split('/')[-1].split('.')[0]
            distance = d.split(',')[1].strip()
            output_txt += f'{filename}, {target_file}, {distance}\n'
    with open(output_dir + '/collated.txt', 'w') as outfile:
        outfile.write(output_txt)
    print('Complete')


# testpoints1 = load_pointmap(OUTPUT_DIRECTORY + '1.webm.txt')
# testpoints2 = load_pointmap(OUTPUT_DIRECTORY + '1_copy.webm.txt')
# z = analytics.dtw_distance_i(testpoints1, testpoints2, 3)
# a = analytics.dtw_distance_d(testpoints1, testpoints2)


IMAGE_SOURCE_DIRECTORY = os.getcwd() + '/test-files/'
PTMAP_SOURCE_DIRECTORY = IMAGE_SOURCE_DIRECTORY + 'output/'
DTW_SOURCE_DIRECTORY = IMAGE_SOURCE_DIRECTORY + 'dtw-out/'
COLLATE_SOURCE_DIRECTORY = IMAGE_SOURCE_DIRECTORY + 'collate-out/'


# image_files = get_files_list(SOURCE_DIRECTORY)
process_video_pointmaps(get_files_list(IMAGE_SOURCE_DIRECTORY), PTMAP_SOURCE_DIRECTORY)
process_dtw_crossover(get_files_list(PTMAP_SOURCE_DIRECTORY), DTW_SOURCE_DIRECTORY)
collate_dtw_data(get_files_list(DTW_SOURCE_DIRECTORY), COLLATE_SOURCE_DIRECTORY)

