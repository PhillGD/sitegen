import unittest
from blockmarkdown import *

class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
            blocks
        )

    def test_markdown_to_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
Same paragraph.
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\nSame paragraph."
            ],
            blocks
        )

    def test_markdown_to_blocks_extra_lines_odd(self):
        markdown = """
# This is a heading



This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."
            ],
            blocks
        )
    
    def test_markdown_to_blocks_extra_lines_even(self):
        markdown = """
# This is a heading




This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."
            ],
            blocks
        )

    def test_markdown_to_blocks_extra_spaces(self):
        markdown = """  
 # This is a heading   
    
  
    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.    
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."
            ],
            blocks
        )
    
    def test_markdown_to_blocks_weird_newlines(self):
        markdown = """
 # This is a heading    \n
    \n
\n
 \n     \n
 This is a paragraph of text. It has some **bold** and _italic_ words inside of it.    
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."
            ],
            blocks
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        block = "This is just a line of text"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, block_type)
    
    def test_block_to_block_type_heading2(self):
        block = "###### This is also a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, block_type)
    
    def test_block_to_block_type_heading3(self):
        block = "####### This is not a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_heading4(self):
        block = "######This is not a valid heading"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)
    
    def test_block_to_block_type_code(self):
        block = "```this is code```"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, block_type)

    def test_block_to_block_type_code2(self):
        block = "```this is code\nand so is this```"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, block_type)

    def test_block_to_block_type_code3(self):
        block = "```this is not valid code``` because of this"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)
    
    def test_block_to_block_type_code4(self):
        block = "``this is not valid code```"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_quote(self):
        block = ">This is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_block_to_block_type_quote2(self):
        block = ">This is a quote\n>So is this"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, block_type)
    
    def test_block_to_block_type_quote3(self):
        block = ">This is a quote\nBut this isn't"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_unordered(self):
        block = "- This is an unordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.ULIST, block_type)

    def test_block_to_block_type_unordered2(self):
        block = "* This is an unordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.ULIST, block_type)
    
    def test_block_to_block_type_unordered3(self):
        block = "- This is an unordered list\n- So is this"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.ULIST, block_type)
    
    def test_block_to_block_type_unordered4(self):
        block = "* This is an invalid unordered list\n- Because of this"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_unordered5(self):
        block = "-This is an invalid unordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_unordered6(self):
        block = "- This is an invalid unordered list\n Because of this"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_ordered(self):
        block = "1. This is an ordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.OLIST, block_type)

    def test_block_to_block_type_ordered2(self):
        block = "1. This is an ordered list\n2. So is this"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.OLIST, block_type)
    
    def test_block_to_block_type_ordered3(self):
        block = "1. This is an invalid ordered list\nBecause of this"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)
    
    def test_block_to_block_type_ordered4(self):
        block = "1. This is an invalid ordered list\n1. Because of this"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_ordered5(self):
        block = "1.This is an invalid ordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_ordered6(self):
        block = "1. This is an invalid ordered list\n2.Because of this"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_ordered7(self):
        block = "1. This is an invalid ordered list\n3. Because of this"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

class TestBlockToHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        markdown = """
This is **bolded** paragraph
text in a p
tag here

"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )
    
    def test_paragraphs(self):
        markdown = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        markdown = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        markdown = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        markdown = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        markdown = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )