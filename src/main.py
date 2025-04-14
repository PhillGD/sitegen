import os
import shutil

from copycontents import copy_files
from sitegen import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_file = "template.html"

def main():
    print("Removing public directory")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying contents of static directory to public directory")
    copy_files(dir_path_static, dir_path_public)

    generate_pages_recursive(dir_path_content, template_file, dir_path_public)

if __name__=="__main__":
    main()