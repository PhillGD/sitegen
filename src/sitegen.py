import os
from pathlib import Path
from blockmarkdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No h1 heading found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating from {from_path} to {dest_path} using {template_path}")
    f = open(from_path, 'r')
    markdown = f.read()
    f.close()

    f = open(template_path, 'r')
    template = f.read()
    f.close()

    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    title = extract_title(markdown)
    new_template = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    new_template = new_template.replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    f = open(dest_path, 'x')
    f.write(new_template)
    f.close

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
        