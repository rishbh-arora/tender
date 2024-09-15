import os
def get_latest_file(download_dir):
    files = os.listdir(download_dir)
    print(files)
    paths = [os.path.join(download_dir, file) for file in files if not file.startswith('.')]
    print(paths)
    a = max(paths, key=os.path.getctime)
    print(a)
    return a

get_latest_file("/home/rishab/Desktop/lunux/Code/repos/tender/tender/zip")