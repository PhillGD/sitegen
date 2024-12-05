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
    def test_to_html_empty_props(self):
        node = LeafNode("p", "text", {})
        self.assertEqual("<p>text</p>", node.to_html())
    def test_to_html(self):
        node = LeafNode("a", "text", {"href": "https://www.google.com"})
        self.assertEqual('<a href="https://www.google.com">text</a>', node.to_html())
    def test_repr(self):
        node = LeafNode("a", "text", {"href": "https://www.google.com"})
        self.assertEqual(
            "LeafNode(a, text, Props: {'href': 'https://www.google.com'})",
            repr(node)
        )

class TestParentNode(unittest.TestCase):
    def test_to_html_none_tag(self):
        node = ParentNode(None, [LeafNode("b", "Bold text")], None)
        self.assertRaises(ValueError, node.to_html)
    def test_to_html_none_children(self):
        node = ParentNode("p", None, None)
        self.assertRaises(ValueError, node.to_html)
    def test_to_html_empty_children(self):
        node = ParentNode("p", [], None)
        self.assertRaises(ValueError, node.to_html)
    def test_to_html_none_props(self):
        node = ParentNode("p", [LeafNode("b", "Bold text")], None)
        self.assertEqual("<p><b>Bold text</b></p>", node.to_html())
    def test_to_html_child_none_tag(self):
        node = ParentNode("p", [LeafNode(None, "text")], None)
        self.assertEqual("<p>text</p>", node.to_html())
    def test_to_html_child_none_value(self):
        node = ParentNode("p", [LeafNode("b", None)], None)
        self.assertRaises(ValueError, node.to_html)
    def test_to_html_props(self):
        node = ParentNode("a", [LeafNode("b", "Bold text")], {"href": "https://www.google.com"})
        self.assertEqual('<a href="https://www.google.com"><b>Bold text</b></a>', node.to_html())
    def test_to_html_child_props(self):
        node = ParentNode("p", [LeafNode("a", "Link text", {"href": "https://www.google.com"})], None)
        self.assertEqual('<p><a href="https://www.google.com">Link text</a></p>', node.to_html())
    def test_to_html_multi_children(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode("i", "Italic text")], None)
        self.assertEqual("<p><b>Bold text</b><i>Italic text</i></p>", node.to_html())
    def test_to_html_nested_parent(self):
        node = ParentNode("p", [ParentNode("b", [LeafNode("i", "Italic text")])], None)
        self.assertEqual("<p><b><i>Italic text</i></b></p>", node.to_html())
    def test_to_html_nested_parent_multi_children(self):
        node = ParentNode("p", [ParentNode("b", [LeafNode("i", "Italic text"), LeafNode(None, "text")])], None)
        self.assertEqual("<p><b><i>Italic text</i>text</b></p>", node.to_html())
    def test_to_html_nested_parent_multi_branches(self):
        node = ParentNode("p", [ParentNode("b", [LeafNode("i", "Italic text")]), LeafNode(None, "text")], None)
        self.assertEqual("<p><b><i>Italic text</i></b>text</p>", node.to_html())
    def test_to_html_multi_nested_parent(self):
        node = ParentNode("p", [ParentNode("b", [LeafNode(None, "text")]), ParentNode("i", [LeafNode(None, "text")])], None)
        self.assertEqual("<p><b>text</b><i>text</i></p>", node.to_html())
    def test_repr(self):
        node = ParentNode("a", [LeafNode("b", "bold"), LeafNode("i", "italic")], {"href": "https://www.google.com"})
        self.assertEqual(
            "ParentNode(a, Children: [LeafNode(b, bold, Props: None), LeafNode(i, italic, Props: None)], Props: {'href': 'https://www.google.com'})",
            repr(node)
        )