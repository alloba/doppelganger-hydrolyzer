import os
import videoprocessor as vp
import analytics
import util


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


if __name__ == '__main__':
    # These all clearly need to change depending on dataset.
    IMAGE_SOURCE_DIRECTORY = os.getcwd() + '/../_mediastore/wsg/'
    PTMAP_SOURCE_DIRECTORY = os.getcwd() + '/../_mediastore/wsg_analytics/' + 'pointmap-out/'
    DTW_SOURCE_DIRECTORY = os.getcwd() + '/../_mediastore/wsg_analytics/' + 'dtw-out/'
    COLLATE_SOURCE_DIRECTORY = os.getcwd() + '/../_mediastore/wsg_analytics/' + 'collate-out/'

    vp.process_video_pointmaps(util.get_files_list(IMAGE_SOURCE_DIRECTORY), PTMAP_SOURCE_DIRECTORY)
    vp.collate_pointmaps(util.get_files_list(PTMAP_SOURCE_DIRECTORY), COLLATE_SOURCE_DIRECTORY)
    analytics.process_dtw_crossover(util.get_files_list(PTMAP_SOURCE_DIRECTORY), DTW_SOURCE_DIRECTORY)
    analytics.collate_dtw_data(util.get_files_list(DTW_SOURCE_DIRECTORY), COLLATE_SOURCE_DIRECTORY)

    # Find all files that were not able to be converted to rgb averages (only have header, making size = 13)
    # corrupt_files = [(f.split('/')[-1].split('.')[0], os.stat(f).st_size) for f in util.get_files_list(PTMAP_SOURCE_DIRECTORY) if os.stat(f).st_size == 13]
    # for f, size in corrupt_files:
    #     print(f)
