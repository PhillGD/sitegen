import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())
    
    def test_none_props_to_html(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())

    def test_repr(self):
        node = HTMLNode("a", "text", None, {"href": "https://www.google.com"})
        self.assertEqual(
            "HTMLNode(a, text, Children: None, Props: {'href': 'https://www.google.com'})",
            repr(node)
        )