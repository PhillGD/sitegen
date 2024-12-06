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
        leaf_node = LeafNode("b", "Bold text")
        node = ParentNode("p", [leaf_node], None)
        self.assertEqual("<p><b>Bold text</b></p>", node.to_html())

    def test_to_html_props(self):
        leaf_node = LeafNode("b", "Bold text")
        node = ParentNode(
            "a", 
            [leaf_node], 
            {"href": "https://www.google.com"}
        )
        self.assertEqual(
            '<a href="https://www.google.com"><b>Bold text</b></a>', 
            node.to_html()
        )

    def test_to_html_child_none_tag(self):
        leaf_node = LeafNode(None, "text")
        node = ParentNode("p", [leaf_node], None)
        self.assertEqual("<p>text</p>", node.to_html())

    def test_to_html_child_none_value(self):
        leaf_node = LeafNode("b", None)
        node = ParentNode("p", [leaf_node], None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_child_props(self):
        leaf_node = LeafNode(
            "a", 
            "Link text", 
            {"href": "https://www.google.com"}
        )
        node = ParentNode("p", [leaf_node], None)
        self.assertEqual(
            '<p><a href="https://www.google.com">Link text</a></p>', 
            node.to_html()
        )

    def test_to_html_multi_children(self):
        leaf_node_1 = LeafNode("b", "Bold text")
        leaf_node_2 = LeafNode("i", "Italic text")
        node = ParentNode("p", [leaf_node_1, leaf_node_2], None)
        self.assertEqual(
            "<p><b>Bold text</b><i>Italic text</i></p>", 
            node.to_html()
        )

    def test_to_html_nested_parent(self):
        leaf_node = LeafNode("i", "Italic text")
        child_node = ParentNode("b", [leaf_node])
        node = ParentNode("p", [child_node], None)
        self.assertEqual(
            "<p><b><i>Italic text</i></b></p>", 
            node.to_html()
        )

    def test_to_html_nested_parent_multi_children(self):
        leaf_node_1 = LeafNode("i", "Italic text")
        leaf_node_2 = LeafNode(None, "text")
        child_node = ParentNode("b", [leaf_node_1, leaf_node_2])
        node = ParentNode("p", [child_node], None)
        self.assertEqual(
            "<p><b><i>Italic text</i>text</b></p>", 
            node.to_html()
        )

    def test_to_html_nested_parent_multi_branches(self):
        leaf_node_1 = LeafNode("i", "Italic text")
        child_node = ParentNode("b", [leaf_node_1])
        leaf_node_2 = LeafNode(None, "text")
        node = ParentNode("p", [child_node, leaf_node_2], None)
        self.assertEqual(
            "<p><b><i>Italic text</i></b>text</p>", 
            node.to_html()
        )

    def test_to_html_multi_nested_parent(self):
        leaf_node_1 = LeafNode(None, "text")
        leaf_node_2 = LeafNode(None, "text")
        child_node_1 = ParentNode("b", [leaf_node_1])
        child_node_2 = ParentNode("i", [leaf_node_2])
        node = ParentNode("p", [child_node_1, child_node_2], None)
        self.assertEqual(
            "<p><b>text</b><i>text</i></p>", 
            node.to_html()
        )
        
    def test_repr(self):
        leaf_node_1 = LeafNode("b", "bold")
        leaf_node_2 = LeafNode("i", "italic")
        node = ParentNode(
            "a", 
            [leaf_node_1, leaf_node_2], 
            {"href": "https://www.google.com"}
        )
        self.assertEqual(
            "ParentNode(a, Children: [LeafNode(b, bold, Props: None), LeafNode(i, italic, Props: None)], Props: {'href': 'https://www.google.com'})",
            repr(node)
        )