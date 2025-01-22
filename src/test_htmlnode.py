import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_1(self):
        node = HTMLNode("a", "This is a Link", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual('href="https://www.google.com" target="_blank"', node.props_to_html())

    def test_values(self):
        node = HTMLNode("div", "I wish I could read")
        self.assertEqual(node.tag, "div",)
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("p", "What a strange world", None, {"class": "primary"})
        self.assertEqual(node.__repr__(), "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})")

class TestLeafNode(unittest.TestCase):
    def test_to_html_1(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">Click me!</a>')

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")])
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_to_html_props(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")], {"class": "test"})
        self.assertEqual(node.to_html(), '<p class="test"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_to_html_nested_parent(self):
        node = ParentNode("div", [ParentNode("p", [LeafNode("b", "Bold text")])])
        self.assertEqual(node.to_html(), '<div><p><b>Bold text</b></p></div>')

    def test_to_html_nested_parent_with_props(self):
        node = ParentNode("div", [ParentNode("p", [LeafNode("b", "Bold text")])], {"class": "test"})
        self.assertEqual(node.to_html(), '<div class="test"><p><b>Bold text</b></p></div>')

    def test_to_html_nested_parent_with_props_2(self):
        node = ParentNode("div", [ParentNode("p", [LeafNode("b", "Bold text")], {"class": "test"})], {"class": "test"})
        self.assertEqual(node.to_html(), '<div class="test"><p class="test"><b>Bold text</b></p></div>')

    def test_to_html_nested_parent_with_props_value(self):
        node = ParentNode("div", [ParentNode("p", [LeafNode("a", "Click me", {"href": "https://www.boot.dev"})], {"class": "test"})], {"class": "test"})
        self.assertEqual(node.to_html(), '<div class="test"><p class="test"><a href="https://www.boot.dev">Click me</a></p></div>')

    def test_to_html_no_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, lambda: node.to_html())

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()