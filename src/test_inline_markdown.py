import unittest

from inline_markdown import (split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes)
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

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],
            extract_markdown_images(text)
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
            extract_markdown_links(text)
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_nodes_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TEXTTYPE.TEXT)
        matches = split_nodes_link([node])
        self.assertListEqual(matches,  [
            TextNode("This is text with a link ", TEXTTYPE.TEXT),
            TextNode("to boot dev", TEXTTYPE.LINK, "https://www.boot.dev"),
            TextNode(" and ", TEXTTYPE.TEXT),
            TextNode("to youtube", TEXTTYPE.LINK, "https://www.youtube.com/@bootdotdev")])

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TEXTTYPE.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TEXTTYPE.TEXT),
                TextNode("image", TEXTTYPE.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TEXTTYPE.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TEXTTYPE.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TEXTTYPE.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TEXTTYPE.TEXT),
                TextNode("image", TEXTTYPE.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TEXTTYPE.TEXT),
                TextNode(
                    "second image", TEXTTYPE.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TEXTTYPE.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TEXTTYPE.TEXT),
                TextNode("link", TEXTTYPE.LINK, "https://boot.dev"),
                TextNode(" and ", TEXTTYPE.TEXT),
                TextNode("another link", TEXTTYPE.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TEXTTYPE.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_no_links_in_text(self):
        node = TextNode("This text has no links.", TEXTTYPE.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This text has no links.", TEXTTYPE.TEXT)], new_nodes)

    def test_split_links_multiple_links_in_text(self):
        node = TextNode("Here is [one link](https://example.com) and [another link](https://example.org).", TEXTTYPE.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
                TextNode("Here is ", TEXTTYPE.TEXT),
                TextNode("one link", TEXTTYPE.LINK, "https://example.com"),
                TextNode(" and ", TEXTTYPE.TEXT),
                TextNode("another link", TEXTTYPE.LINK, "https://example.org"),
                TextNode(".", TEXTTYPE.TEXT)
            ], new_nodes)

    def test_split_links_at_start(self):
        node = TextNode("[Link at start](https://example.com) and more text.", TEXTTYPE.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
                TextNode("Link at start", TEXTTYPE.LINK, "https://example.com"), 
                TextNode(" and more text.", TEXTTYPE.TEXT)
            ], new_nodes)                   

    def test_split_links_at_end(self):
        node = TextNode("Text before the link [Link](https://example.com)", TEXTTYPE.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
                TextNode("Text before the link ", TEXTTYPE.TEXT), 
                TextNode("Link", TEXTTYPE.LINK, "https://example.com")
            ], new_nodes)

    def test_text_to_textnode(self):
        node = text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(node, [
            TextNode("This is ", TEXTTYPE.TEXT),
            TextNode("text", TEXTTYPE.BOLD),
            TextNode(" with an ", TEXTTYPE.TEXT),
            TextNode("italic", TEXTTYPE.ITALIC),
            TextNode(" word and a ", TEXTTYPE.TEXT),
            TextNode("code block", TEXTTYPE.CODE),
            TextNode(" and an ", TEXTTYPE.TEXT),
            TextNode("obi wan image", TEXTTYPE.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TEXTTYPE.TEXT),
            TextNode("link", TEXTTYPE.LINK, "https://boot.dev"),
            ]
        )       

        
        

     

if __name__ == "__main__":
    unittest.main()