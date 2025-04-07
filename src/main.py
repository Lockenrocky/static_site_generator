import sys
from textnode import *
import os, shutil
from block_markdown import *

def extract_title(markdown):
    lines = markdown_to_blocks(markdown)
    for line in lines:
        if line.startswith("# "):
            return line.strip("# ")
    raise Exception("No h1 found in markdown")

def generate_page(from_path, template_path, dest_path, BASEPATH):
    bp = BASEPATH
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = open(from_path)
    html_text = md.read()
    md.close()
    title = extract_title(html_text)
    html_text = markdown_to_html_node(html_text)
    template_md = open(template_path, mode="r")
    template = template_md.read()
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html_text)
    template = template.replace('href="/', 'href="' + bp).replace('src="/', 'src="' + bp)
    template_md.close()
    file_name = from_path.split("/")[-1].replace(".md",".html")
    file_path = dest_path + "/" + file_name
    with open(file_path, "w") as file:
        file.write(template)
    return

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    
    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(file_path):
            generate_page(file_path, template_path, dest_dir_path, basepath)
        elif os.path.isdir(file_path):
            dir_path = os.path.join(dest_dir_path, filename)
            os.mkdir(dir_path)
            generate_pages_recursive(file_path, template_path, dir_path, basepath)

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

def copy_from_source_to_destination(src_path, des_path):
    # delete every file inside the public folder 
    if len(os.listdir(des_path)) > 0:
        clear_directory(des_path)
    # recursivly copy all files and subdirectories, nested files, etc.
    for filename in os.listdir(src_path):
        file_path = os.path.join(src_path, filename)
        if os.path.isfile(file_path):
            shutil.copy(file_path, des_path)
        elif os.path.isdir(file_path):
            dir_path = os.path.join(des_path, filename)
            os.mkdir(dir_path)
            copy_from_source_to_destination(file_path,dir_path)

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    
    copy_from_source_to_destination("static", "docs")
    generate_pages_recursive("content", "template.html", "docs/", basepath)

    #copy_from_source_to_destination("/home/lockenrocky/workspace/github.com/Lockenrocky/static_site_generator/static", 
    #                                "/home/lockenrocky/workspace/github.com/Lockenrocky/static_site_generator/public")
    #generate_pages_recursive("/home/lockenrocky/workspace/github.com/Lockenrocky/static_site_generator/content",
    #              "/home/lockenrocky/workspace/github.com/Lockenrocky/static_site_generator/template.html",
    #              "/home/lockenrocky/workspace/github.com/Lockenrocky/static_site_generator/public/")
    
main()   