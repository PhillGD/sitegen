import unittest
from blockmarkdown import *

class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
            blocks
        )

    def test_markdown_to_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.
Same paragraph.
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\nSame paragraph."
            ],
            blocks
        )

    def test_markdown_to_blocks_extra_lines_odd(self):
        markdown = """
# This is a heading



This is a paragraph of text. It has some **bold** and *italic* words inside of it.
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
            ],
            blocks
        )
    
    def test_markdown_to_blocks_extra_lines_even(self):
        markdown = """
# This is a heading




This is a paragraph of text. It has some **bold** and *italic* words inside of it.
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
            ],
            blocks
        )

    def test_markdown_to_blocks_extra_spaces(self):
        markdown = """  
 # This is a heading   
    
  
    This is a paragraph of text. It has some **bold** and *italic* words inside of it.    
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
            ],
            blocks
        )
    
    def test_markdown_to_blocks_weird_newlines(self):
        markdown = """
 # This is a heading    \n
    \n
\n
 \n     \n
 This is a paragraph of text. It has some **bold** and *italic* words inside of it.    
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
            ],
            blocks
        )
    
        