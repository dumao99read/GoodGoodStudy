
import os
import time
import pandas as pd
import openpyxl

CURRENT_DIR = os.getcwd()

def get_fileList_by_directory(path, directory, file_types = ['.xlsx','.xlsm']):
    file_path = os.path.join(path, directory)
    file_list = []
    for dirpath, dirnames, filenames in os.walk(file_path):
        # 获取路径下所有文件夹
        # for item in dirnames:
        #     file_list.append(os.path.join(dirpath, item))

        # 获取路径下所有指定类型的文件
        for file in filenames:
            if any(file.lower().endswith(file_type) for file_type in file_types):
                file_list.append(os.path.join(dirpath,file))

    return file_list



if __name__ == '__main__':
    time1 = time.time()
    x = get_fileList_by_directory(CURRENT_DIR, '../fileDemo')
    time2 = time.time()
    print(x)
    print(time2 - time1)
