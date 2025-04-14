import os
from blockmarkdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No h1 heading found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
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

    f = open(dest_path, 'x')
    f.write(new_template)
    f.close