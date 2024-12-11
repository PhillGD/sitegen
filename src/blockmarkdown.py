import re

def markdown_to_blocks(markdown):
        blocks = []
        markdown_blocks = re.split(r"\n\n|\n\s+\n", markdown)
        for markdown_block in markdown_blocks:
            if markdown_block != "" and not markdown_block.isspace():
                  blocks.append(markdown_block.strip())
        return blocks
