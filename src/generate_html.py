import os

from block_markdown import markdown_to_html_node
from htmlnode import ParentNode

def extract_title(markdown):
    split_markdown = markdown.strip().split("\n\n")

    for line in split_markdown:
        if line.strip().startswith("# "):
            return line[2:].strip()
    
    raise ValueError("Invalid HTML: no h1 title")

def generate_page(from_path, template_path, dest_path, basepath):
    # Checking that parameter values are valid   
    if not os.path.isfile(from_path):
        raise ValueError("From path is not a file")
    if not from_path.endswith(".md"):
        raise ValueError("From path file is not a markdown file")
    
    if not os.path.isfile(template_path):
        raise ValueError("Template path is not a file")
    if not template_path.endswith(".html"):
        raise ValueError("Template path file is not a html file")
    
    if not dest_path.endswith(".html"):
        raise ValueError("Destination file will not be an html file")

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = None
    with open(from_path) as f:
        markdown = f.read()

    template = None
    with open(template_path) as f:
        template = f.read()
    
    title = extract_title(markdown)
    html_body = markdown_to_html_node(markdown).to_html()

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_body).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    # Make destination directories
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as f:
        f.write(page)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # Checking that parameter values are valid   
    if not os.path.exists(dir_path_content):
        raise ValueError("Content does not exist")
    
    if not os.path.isfile(template_path):
        raise ValueError("Template path is not a file")
    if not template_path.endswith(".html"):
        raise ValueError("Template path file is not a html file")
    
    if os.path.isfile(dest_dir_path):
        raise ValueError("Destination is a file")

    # Generating starts here
    for path in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, path)
        dest_path = os.path.join(dest_dir_path, path)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path) and from_path.endswith(".md"):           
            dest_path = dest_path[:-3] + ".html"
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)