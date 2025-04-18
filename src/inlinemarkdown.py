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


def split_nodes_image(old_nodes):
    new_nodes = split_image_link_nodes_helper(old_nodes, TextType.IMAGE)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = split_image_link_nodes_helper(old_nodes, TextType.LINK)
    return new_nodes

def split_image_link_nodes_helper(old_nodes, TextType):
    new_nodes = []
    match TextType:
        case TextType.IMAGE:
            delimiter_opening = "!["
            extract_markdown = extract_markdown_images
        case TextType.LINK:
            delimiter_opening = "["
            extract_markdown = extract_markdown_links
        case _:
            raise ValueError("TextType must be Link or Image")
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            original_text = old_node.text
            nodes = extract_markdown(original_text)
            if len(nodes) == 0:
                new_nodes.append(old_node)
            else:
                for node in nodes:
                    sections = original_text.split(f"{delimiter_opening}{node[0]}]({node[1]})", 1)
                    if len(sections) != 2:
                        raise ValueError("Invalid markdown: Closing image delimiters not found.")
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(node[0], TextType, node[1]))
                    original_text = sections[1]
                if original_text != "":
                    new_nodes.append(TextNode(original_text, TextType.TEXT))
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

def text_to_textnodes(text):
    return (
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_link(
                        split_nodes_image([TextNode(text, TextType.TEXT)])
                    ), "`", TextType.CODE
                ), "**", TextType.BOLD
            ), "_", TextType.ITALIC
        )
    )