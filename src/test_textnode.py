import unittest

from textnode import TextNode, TEXTTYPE, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TEXTTYPE.BOLD)
        node2 = TextNode("This is a text node", TEXTTYPE.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):    
        node = TextNode("This is a text node", TEXTTYPE.BOLD, None)
        node2 = TextNode("This is a text node", TEXTTYPE.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false_1(self):
        node = TextNode("This is a text node", TEXTTYPE.BOLD)
        node2 = TextNode("This is a text node", TEXTTYPE.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_false_2(self):
        node = TextNode("This is a text node", TEXTTYPE.BOLD, None)
        node2 = TextNode("This is a text node", TEXTTYPE.BOLD, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TEXTTYPE.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_text(self):
        node = text_node_to_html_node(TextNode("This is a beautiful text", TEXTTYPE.TEXT))
        self.assertEqual(node.to_html(), "This is a beautiful text")

    def test_text_node_to_bold(self):
        node = text_node_to_html_node(TextNode("This is a beautiful text", TEXTTYPE.BOLD))
        self.assertEqual(node.to_html(), "<b>This is a beautiful text</b>")

    def test_text_node_to_italic(self):
        node = text_node_to_html_node(TextNode("This is a beautiful text", TEXTTYPE.ITALIC))
        self.assertEqual(node.to_html(), "<i>This is a beautiful text</i>")

    def test_text_node_to_code(self):
        node = text_node_to_html_node(TextNode("This is a beautiful text", TEXTTYPE.CODE))
        self.assertEqual(node.to_html(), "<code>This is a beautiful text</code>")

    def test_text_node_to_link(self):
        node = text_node_to_html_node(TextNode("This is a beautiful text", TEXTTYPE.LINK, "https://www.boot.dev"))
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">This is a beautiful text</a>')

    def test_text_node_to_image(self):
        node = text_node_to_html_node(TextNode("This is a beautiful text", TEXTTYPE.IMAGE, "https://www.boot.dev"))
        self.assertEqual(node.to_html(), '<img src="https://www.boot.dev" alt="Image of a yellow flower"></img>')          

if __name__ == "__main__":
    unittest.main()