import os
import shutil

def copy_directory_recursively(source, destination):
    # Checking that parameter values are valid   
    if not os.path.exists(source):
        raise ValueError("Source does not exist")
    if os.path.isfile(source):
        raise ValueError("Source is a file not a directory")
    if os.path.isfile(destination):
        raise ValueError("Destination is a file not a directory")

    # Create the destination folder
    if not os.path.exists(destination):
        os.mkdir(destination)

    # Copying starts here
    for path in os.listdir(source):
        from_path = os.path.join(source, path)
        dest_path = os.path.join(destination, path)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):           
            shutil.copy(from_path, dest_path)
        else:
            copy_directory_recursively(from_path, dest_path)