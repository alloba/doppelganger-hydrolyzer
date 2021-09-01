from dtw import *
from multiprocessing import Pool, Process
import multiprocessing
import videoprocessor
import os


def dtw_distance_d(series1, series2):
    try:
        alignment = dtw(series1, series2, keep_internals=True)  # not sure if keep internals is required.
        return alignment.distance
    except Exception as e:
        print(f'failed for {str(series1)} and {str(series2)}')
        raise e


def dtw_distance_i(series1, series2, dimensionality=0):
    distances = []
    for i in range(dimensionality):
        s1 = [x[i] for x in series1]
        s2 = [z[i] for z in series2]
        distances.append(dtw(s1, s2).distance)
    return sum(distances)


# For all data data collections, run DTW calculations against all of them.
# Output will be stored in files with the name of the comparing file.
# Meaning, for files a,b,c there will be 3 files named a,b,c with 3 distances + filenames inside.
def process_dtw_crossover(pointmap_file_list, output_dir):
    print(f'Processing DTW values for {len(pointmap_file_list)} files...')
    print(f'Outputting results to {output_dir}')
    pool = Pool(multiprocessing.cpu_count() - 1)
    for i in range(len(pointmap_file_list)):
        pool.apply_async(process_single_dtw, args=(pointmap_file_list, output_dir, i))
    pool.close()
    pool.join()
    print('\n')


def process_single_dtw(pointmap_file_list, output_dir, index):
    print(f'{index}/{len(pointmap_file_list)} DTW', end='\r')
    output_text = 'target, dtw\n'

    if os.path.isfile(output_dir + pointmap_file_list[index].split('/')[-1].split('.')[0] + '.csv'):
        return

    with open(output_dir + pointmap_file_list[index].split('/')[-1].split('.')[0] + '.csv', 'w') as out_file:
        out_file.write(output_text)

        for j in pointmap_file_list:
            ii = videoprocessor.load_pointmap(pointmap_file_list[index])
            jj = videoprocessor.load_pointmap(j)
            dist = dtw_distance_d(ii, jj)
            out_file.write(f"{j.split('/')[-1].split('.')[0]}, {dist}\n")


def collate_dtw_data(dtw_files_list, output_dir):
    print('Collating results into single file...')
    output_txt = 'source,target,weight\n'

    with open(output_dir + '/collated-dtw.csv', 'w') as outfile:
        outfile.write(output_txt)
        z = 0
        for f in dtw_files_list:
            z += 1
            print(f'{z}/{len(dtw_files_list)}', end='\r')
            filename = f.split('/')[-1].split('.')[0]
            ff = open(f, 'r')
            data = ff.readlines()[1:]
            for d in data:
                target_file = d.split(',')[0].strip().split('/')[-1].split('.')[0]
                distance = d.split(',')[1].strip()
                outfile.write(f'{filename}, {target_file}, {distance}\n')
        print('Complete')
