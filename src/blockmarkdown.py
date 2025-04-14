import re
from enum import Enum

from htmlnode import ParentNode
from inlinemarkdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
        blocks = []
        markdown_blocks = re.split(r"\n\n|\n\s+\n", markdown)
        for markdown_block in markdown_blocks:
            if markdown_block != "" and not markdown_block.isspace():
                  blocks.append(markdown_block.strip())
        return blocks

def block_to_block_type(block):

    lines = block.split("\n")
              
    match block:
        case block if re.match(r"^#{1,6}\s.*", block):
            return BlockType.HEADING
        case block if re.match(r"^`{3}((.|\n)*)`{3}$", block):
            return BlockType.CODE
        case block if re.match(r">.*", block):
            for line in lines:
                if not re.match(r">.*", line):
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE
        case block if re.match(r"^(\*|-)\s.*", block):
            ulist_char = f"\\{block[0]}"
            for line in lines:
                if not re.match(rf"^{ulist_char}\s.*", line):
                    return BlockType.PARAGRAPH
            return BlockType.ULIST
        case block if re.match(r"^1\.\s.*", block):
            for i in range(len(lines)):
                if not re.match(rf"^{[i + 1]}\.\s.*", lines[i]):
                    return BlockType.PARAGRAPH
            return BlockType.OLIST
        case _:
            return BlockType.PARAGRAPH
        
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case block_type if block_type == BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case block_type if block_type == BlockType.HEADING:
            return heading_to_html_node(block)
        case block_type if block_type == BlockType.CODE:
            return code_to_html_node(block)
        case block_type if block_type == BlockType.QUOTE:
            return quote_to_html_node(block)
        case block_type if block_type == BlockType.ULIST:
            return ulist_to_html_node(block)
        case block_type if block_type == BlockType.OLIST:
            return olist_to_html_node(block)
        case _:
            raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level +1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)