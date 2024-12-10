import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            inner_nodes = []
            string_list = old_node.text.split(delimiter)
            if len(string_list) % 2 == 0:
                raise ValueError(f"Invalid markdown: Closing delimiter {delimiter} not found.")
            for i in range(len(string_list)):
                if string_list[i] != "":
                    if i % 2 == 0:
                        inner_nodes.append(TextNode(string_list[i], TextType.TEXT))
                    else:
                        inner_nodes.append(TextNode(string_list[i], text_type))
            new_nodes.extend(inner_nodes)
    return new_nodes

def extract_markdown_images(text):
    if len(text) == 0:
        raise ValueError("No text provided")
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_markdown_links(text):
    if len(text) == 0:
        raise ValueError("No text provided")
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links