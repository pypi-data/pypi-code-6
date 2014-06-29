import os

__author__ = 'maruf'



def get_files(rootdir):
    file_list = []
    for root, subFolders, files in os.walk(rootdir):
        for filename in files:
            filePath = os.path.join(root, filename)
            file_list.append(filePath)

    return file_list


if __name__ == "__main__":
    path = "/home/maruf/devenv/dist"
    file_list = get_files(path)
    root_len = len(path)
    for filename in file_list:
        relative = filename[root_len:]
        print filename, " ", relative