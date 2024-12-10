import unittest
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq_text_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is also a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_type_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_none_url_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_eq_url_false(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dave")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, bold, https://www.boot.dev)", 
            repr(node)
        )

class TestTextNodeToHTML(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        node = TextNode("Text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(None, html_node.tag)
        self.assertEqual("Text", html_node.value)
        self.assertEqual(None, html_node.props)
    
    def test_text_node_to_html_node_bold(self):
        node = TextNode("Bold Text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual("b", html_node.tag)
        self.assertEqual("Bold Text", html_node.value)
        self.assertEqual(None, html_node.props)
    
    def test_text_node_to_html_node_italic(self):
        node = TextNode("Italic Text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual("i", html_node.tag)
        self.assertEqual("Italic Text", html_node.value)
        self.assertEqual(None, html_node.props)

    def test_text_node_to_html_node_code(self):
        node = TextNode("Code Text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual("code", html_node.tag)
        self.assertEqual("Code Text", html_node.value)
        self.assertEqual(None, html_node.props)

    def test_text_node_to_html_node_link(self):
        node = TextNode("Link Text", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual("a", html_node.tag)
        self.assertEqual("Link Text", html_node.value)
        self.assertEqual({"href": "https://www.google.com"}, html_node.props)
    
    def test_text_node_to_html_node_image(self):
        node = TextNode("Image Text", TextType.IMAGE, "https://www.google.com/logos/doodles")
        html_node = text_node_to_html_node(node)
        self.assertEqual("img", html_node.tag)
        self.assertEqual("", html_node.value)
        self.assertEqual(
            {"src": "https://www.google.com/logos/doodles", "alt": "Image Text"}, 
            html_node.props
        )

    def test_text_node_to_html_node_none(self):
        node = TextNode("Text", None, "https://www.google.com")
        self.assertRaises(ValueError, text_node_to_html_node, node)


if __name__=="__main__":
    unittest.main()