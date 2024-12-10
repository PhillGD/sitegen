import unittest
from inlinemarkdown import *

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_delimiter_text_only(self):
        node = TextNode("Text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertListEqual([TextNode("Text", TextType.TEXT)], new_nodes)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("The word **bold** is bold", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("The word ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" is bold", TextType.TEXT)
            ], 
            new_nodes
        )

    def test_split_nodes_delimiter_bold_start(self):
        node = TextNode("**Bold** is a bold word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Bold", TextType.BOLD),
                TextNode(" is a bold word", TextType.TEXT)
            ], 
            new_nodes
        )
    
    def test_split_nodes_delimiter_bold_multi(self):
        node = TextNode("The word **bold** should be a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("The word ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" should be a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ], 
            new_nodes
        )

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("The word *italic* is italic", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("The word ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" is italic", TextType.TEXT)
            ], 
            new_nodes
        )

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This `code block text` is a code block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This ", TextType.TEXT),
                TextNode("code block text", TextType.CODE),
                TextNode(" is a code block", TextType.TEXT)
            ], 
            new_nodes
        )

    def test_split_nodes_delimiter_bold_and_italic(self):
        node = TextNode("This is **bold** and *italic* together", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes2 = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" together", TextType.TEXT)
            ], 
            new_nodes2
        )
    
    def test_split_nodes_delimiter_bold_node(self):
        node = TextNode("All bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([TextNode("All bold text", TextType.BOLD)], new_nodes)
    
    def test_split_nodes_delimiter_multiple_bold_nodes(self):
        node = TextNode("All bold text", TextType.BOLD)
        node2 = TextNode("Also all bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("All bold text", TextType.BOLD),
                TextNode("Also all bold", TextType.BOLD)
            ], 
            new_nodes
        )
    
    def test_split_nodes_delimiter_multiple_type_nodes(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        node2 = TextNode("This is all bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        self.assertListEqual(
            [   
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
                TextNode("This is all bold", TextType.BOLD)
            ], 
            new_nodes
        )
    
    def test_split_nodes_delimiter_open_delimiter(self):
        node = TextNode("Unclosed **bold text delimiters", TextType.TEXT)
        self.assertRaises(ValueError, split_nodes_delimiter, [node], "**", TextType.BOLD)

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        text = "This is an image ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        images = extract_markdown_images(text)
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif")], images)
    
    def test_extract_markdown_images_multi(self):
        text = "This is an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and so is this ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ], 
            images
        )
    
    def test_extract_markdown_images_none(self):
        text = "No images here"
        images = extract_markdown_images(text)
        self.assertListEqual([], images)

    def test_extract_markdown_images_none(self):
        text = ""
        self.assertRaises(ValueError, extract_markdown_images, text)

    def test_extract_markdown_links_single(self):
        text = "This is a link [to boot dev](https://www.boot.dev)"
        links = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], links)
    
    def test_extract_markdown_links_multi(self):
        text = "This is a link [to boot dev](https://www.boot.dev) and so is this [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ], 
            links
        )
    
    def test_extract_markdown_links_none(self):
        text = "No links here"
        links = extract_markdown_links(text)
        self.assertListEqual([], links)

    def test_extract_markdown_links_none(self):
        text = ""
        self.assertRaises(ValueError, extract_markdown_links, text)

if __name__=="__main__":
    unittest.main()