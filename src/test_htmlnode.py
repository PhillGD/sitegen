import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())
    
    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())

    def test_repr(self):
        node = HTMLNode("a", "text", None, {"href": "https://www.google.com"})
        self.assertEqual(
            "HTMLNode(a, text, Children: None, Props: {'href': 'https://www.google.com'})",
            repr(node)
        )

class TestLeafNode(unittest.TestCase):
    def test_to_html_none_value(self):
        node = LeafNode("p", None, {"href": "https://www.google.com"})
        self.assertRaises(ValueError, node.to_html)
    def test_to_html_none_tag(self):
        node = LeafNode(None, "text", {"href": "https://www.google.com"})
        self.assertEqual("text", node.to_html())
    def test_to_html_none_props(self):
        node = LeafNode("p", "text", None)
        self.assertEqual("<p>text</p>", node.to_html())
    def test_to_html(self):
        node = LeafNode("a", "text", {"href": "https://www.google.com"})
        self.assertEqual('<a href="https://www.google.com">text</a>', node.to_html())