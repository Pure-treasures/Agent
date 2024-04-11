import os
import shutil
from pathlib import Path
from fastapi import UploadFile
from pypinyin import lazy_pinyin

PARENT_DIR = os.path.dirname(os.path.dirname(__file__))

def get_metadata_dir():
    return os.path.join(PARENT_DIR, "metadata")

def generate_user_workspace_dir(user_token: str) -> str:
    workspace_dir = Path(os.path.join(get_metadata_dir(), user_token))
    workspace_dir.mkdir(parents=True, exist_ok=True)
    return workspace_dir.__str__()

def remove_user_workspace_dir(user_token: str):
    workspace_dir = Path(os.path.join(get_metadata_dir(), user_token))
    if not Path(workspace_dir).exists():
        return
    shutil.rmtree(workspace_dir)

def save_upload_file(upload_file: UploadFile, destination_path: str):
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    with open(destination_path, "wb") as file_object:
        file_object.write(upload_file.file.read())
        
def to_pinyin_100(name: str) -> str :
    return "".join(lazy_pinyin(name))[:100]

def get_filename_extension(filename):
    _, extension = os.path.splitext(filename)
    return extension[1:]

def get_filename(file_path):
    file_name = os.path.basename(file_path)
    return file_name