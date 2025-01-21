import unittest

from textnode import TextNode, TEXTTYPE

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TEXTTYPE.BOLD)
        node2 = TextNode("This is a text node", TEXTTYPE.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TEXTTYPE.BOLD, None)
        node2 = TextNode("This is a text node", TEXTTYPE.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TEXTTYPE.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TEXTTYPE.BOLD, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TEXTTYPE.BOLD)
        node2 = TextNode("This is a text node", TEXTTYPE.ITALIC)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TEXTTYPE.BOLD, None)
        node2 = TextNode("This is a text node", TEXTTYPE.BOLD, "https://boot.dev")
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node!", TEXTTYPE.BOLD, None)
        node2 = TextNode("This is a text node", TEXTTYPE.BOLD)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()