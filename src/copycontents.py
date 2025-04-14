import shutil
import os

def copy_files(source, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    for filename in os.listdir(source):
        src_path = os.path.join(source, filename)
        dest_path = os.path.join(dest, filename)
        print(f"{src_path} -> {dest_path}")
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_files(src_path, dest_path)