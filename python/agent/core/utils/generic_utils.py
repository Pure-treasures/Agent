import os
from typing import List
from pypinyin import lazy_pinyin

def to_pinyin_100(name: str) -> str :
    return "".join(lazy_pinyin(name))[:100]

def get_filename_extension(filename):
    _, extension = os.path.splitext(filename)
    return extension[1:]

def get_filename(file_path):
    file_name = os.path.basename(file_path)
    return file_name

def clear_directory(path: str):
    if os.path.exists(path) and os.path.isdir(path):
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                clear_directory(file_path)
    else:
        raise (NotADirectoryError, FileNotFoundError)

def get_all_files_in_directory(directory: str) -> List[str]:
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files