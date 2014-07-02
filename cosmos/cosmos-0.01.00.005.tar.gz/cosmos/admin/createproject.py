import os
import base64
import sampleprojectdef

__author__ = 'Maruf Maniruzzaman'

def new_project(path):
    file_data_list = sampleprojectdef.file_data_list
    for file_data in file_data_list:
        filename = file_data["name"]
        data = file_data["data"]
        if filename[0]=='/':
            filename = filename[1:]
        file_path = os.path.join(path, filename)
        dir_name = os.path.dirname(file_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(file_path, 'w') as content_file:
            content_file.write(data)

if __name__ == "__main__":
    path = os.getcwd()
    new_project(path)

