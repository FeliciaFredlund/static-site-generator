import os
import shutil

from copystatic import copy_directory_recursively
from generate_html import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content_index = "./content"
dir_path_template = "template.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_directory_recursively(dir_path_static, dir_path_public)

    # Generating html page from markdown files in ./content
    generate_pages_recursive(dir_path_content_index, dir_path_template, dir_path_public)

main()