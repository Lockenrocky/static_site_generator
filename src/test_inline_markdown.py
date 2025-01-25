import unittest

from inline_markdown import (split_nodes_delimiter)
from textnode import TextNode, TEXTTYPE

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TEXTTYPE.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TEXTTYPE.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TEXTTYPE.TEXT),
                TextNode("bolded", TEXTTYPE.BOLD),
                TextNode(" word", TEXTTYPE.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TEXTTYPE.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TEXTTYPE.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TEXTTYPE.TEXT),
                TextNode("bolded", TEXTTYPE.BOLD),
                TextNode(" word and ", TEXTTYPE.TEXT),
                TextNode("another", TEXTTYPE.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TEXTTYPE.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TEXTTYPE.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TEXTTYPE.TEXT),
                TextNode("bolded word", TEXTTYPE.BOLD),
                TextNode(" and ", TEXTTYPE.TEXT),
                TextNode("another", TEXTTYPE.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TEXTTYPE.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TEXTTYPE.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TEXTTYPE.TEXT),
                TextNode("italic", TEXTTYPE.ITALIC),
                TextNode(" word", TEXTTYPE.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TEXTTYPE.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TEXTTYPE.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TEXTTYPE.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TEXTTYPE.BOLD),
                TextNode(" and ", TEXTTYPE.TEXT),
                TextNode("italic", TEXTTYPE.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TEXTTYPE.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TEXTTYPE.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TEXTTYPE.TEXT),
                TextNode("code block", TEXTTYPE.CODE),
                TextNode(" word", TEXTTYPE.TEXT),
            ],
            new_nodes,
        )
       
if __name__ == "__main__":
    unittest.main()