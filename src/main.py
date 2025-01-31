from textnode import *
import os, shutil

def clear_directory(path):
    folder = path
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def copy_from_source_to_destination():
    # delete every file inside the public folder 
    des_path = "/home/lockenrocky/workspace/github.com/Lockenrocky/static_site_generator/public"
    if len(os.listdir(des_path)) > 0:
        clear_directory(des_path)
    # recursivly copy all files and subdirectories, nested files, etc.
    folder = "/home/lockenrocky/workspace/github.com/Lockenrocky/static_site_generator/static"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                shutil.copy(file_path, des_path)
                print(f"copied file from {file_path} to {des_path}")
            elif os.path.isdir(file_path):
                folder = file_path
                copy_from_source_to_destination()
        except Exception as e:
            print(f"error: {e}")


def main():
    copy_from_source_to_destination()
    
main()   