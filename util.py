import os


def get_files_list(directory):
    dir_sanitized = directory if directory.endswith("/") else directory + '/'
    if directory is None:
        files = os.listdir('')
    else:
        files = os.listdir(directory)

    return [dir_sanitized + x for x in files if os.path.isfile(dir_sanitized + x)]
