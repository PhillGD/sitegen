import os
import shutil

from copycontents import copy_files

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    print("Removing public directory")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying contents of static directory to public directory")
    copy_files(dir_path_static, dir_path_public)

if __name__=="__main__":
    main()