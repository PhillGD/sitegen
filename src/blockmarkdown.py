import re

def markdown_to_blocks(markdown):
        blocks = []
        markdown_blocks = re.split(r"\n\n|\n\s+\n", markdown)
        for markdown_block in markdown_blocks:
            if markdown_block != "" and not markdown_block.isspace():
                  blocks.append(markdown_block.strip())
        return blocks

def block_to_block_type(block):
    block_type_paragraph = "paragraph"
    block_type_heading = "heading"
    block_type_code = "code"
    block_type_quote = "quote"
    block_type_ulist = "unordered_list"
    block_type_olist = "ordered_list"

    lines = block.split("\n")
              
    match block:
        case block if re.match(r"^#{1,6}\s.*", block):
            return block_type_heading
        case block if re.match(r"^`{3}((.|\n)*)`{3}$", block):
            return block_type_code
        case block if re.match(r">.*", block):
            for line in lines:
                if not re.match(r">.*", line):
                    return block_type_paragraph
            return block_type_quote
        case block if re.match(r"^(\*|-)\s.*", block):
            for line in lines:
                if not re.match(r"^(\*|-)\s.*", line):
                    return block_type_paragraph
            return block_type_ulist
        case block if re.match(r"^1\.\s.*", block):
            for i in range(len(lines)):
                if not re.match(rf"^{[i + 1]}\.\s.*", lines[i]):
                    return block_type_paragraph
            return block_type_olist
        case _:
            return block_type_paragraph

