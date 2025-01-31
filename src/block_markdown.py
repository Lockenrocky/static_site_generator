import re
from textnode import (text_node_to_html_node)
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import (text_to_textnodes)

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown):
    block_strings = list(filter(None, list(map(lambda x: x.strip(), markdown.split("\n\n")))))
    return block_strings

def block_to_block_type(md_block):
    if re.search("^#{1,6} .*", md_block):
        return block_type_heading
    if re.search("^```\n.*\n```$", md_block, flags=re.M):
        return block_type_code
    if re.search("^> ", md_block):
        return block_type_quote
    if re.search("^[*-] .*", md_block):
        return block_type_ulist
    if re.search("^[1-9]. .*", md_block):
        return block_type_olist
    return block_type_paragraph

def block_text_without_block_type(md_block, block_type):
    if block_type == "heading":
        match = re.search(r"(?!^#{1,6} )([a-zA-Z1-9].+)", md_block)
        return match.group()
    if block_type == "code":
        match = re.search(r"(?!`\n).*(?=\n```)", md_block, flags=re.M)
        return match.group()
    if block_type == "quote":
        match = re.search(r"(?!^> )([a-zA-Z1-9].+)", md_block)
        return match.group()
    if block_type == "ordered_list":
        match = re.search(r"(?!^[1-9]. )([a-zA-Z1-9].+)", md_block)
        return match.group()
    if block_type == "unordered_list":
        match = re.search(r"(?!^[*-] )([a-zA-Z1-9].+)", md_block)
        return match.group()
    return md_block

def markdown_to_html_node(markdown):
    # 1. split your markdown into blocks
    markdown_blocks = markdown_to_blocks(markdown)
    # 2. determine type of each block
    child_nodes = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        # 3. create HTMLNode based on the type of the block
        node = get_HTMLNode_from_block_type(block, block_type)
        if type(node) is list:
            for n in node:
                child_nodes.append(n)
        else:
            child_nodes.append(node)
    return ParentNode("div", child_nodes).to_html()

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_text(block):
    lines = block.split("\n")
    lines = " ".join(lines)
    children = text_to_children(lines)
    return children

def heading_to_text(block):
    list_items = block.split("\n")
    children = []
    for item in list_items:
        header_type = len("".join(filter(lambda x: x == "#", item)))
        child = text_to_children(item[header_type+1:])
        children.append(ParentNode(f"h{header_type}", child, None))
    return children

def code_to_text(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children, None)
    return ParentNode("pre", [code], None)

def quote_to_text(block):
    list_items = block.replace("> ","").split("\n")
    list_items = " ".join(list_items)
    children = text_to_children(list_items)
    return children

def unordered_list_to_text(block):
    list_items = block.split("\n")
    children = []
    for item in list_items:
        child_node = text_to_children(item[2:])
        children.append(ParentNode("li", child_node, None))
    return children

def ordered_list_to_text(block):
    list_items = block.split("\n")
    children = []
    for item in list_items:
        child_node = text_to_children(item[3:])
        children.append(ParentNode("li", child_node, None))
    return children


def get_HTMLNode_from_block_type(block, type):
    # getting block text without block type
    match type:
        case "paragraph":
            child_nodes = paragraph_to_text(block)
            return ParentNode("p",child_nodes, None)
        case "heading":
            return heading_to_text(block)
        case "code":
            return code_to_text(block)
        case "quote":
            child_nodes = quote_to_text(block)
            return ParentNode("blockquote", child_nodes, None)
        case "unordered_list":
            child_nodes = unordered_list_to_text(block)
            return ParentNode("ul", child_nodes, None)
        case "ordered_list":
            child_nodes = ordered_list_to_text(block)
            return ParentNode("ol", child_nodes, None)

    lines = block.split("\n")
    lines = " ".join(lines)
    text = block_text_without_block_type(lines, type)
    # getting childnodes as Textnodes
    child_nodes_text_nodes = text_to_textnodes(text)
    # convert childnodes from Tetxnodes to HTMLNodes
    child_nodes_html_nodes = list(map(lambda x: text_node_to_html_node(x), child_nodes_text_nodes))


    if type == "heading":
        header_type = len("".join(filter(lambda x: x == "#", block)))
        if len(child_nodes_html_nodes) > 0:
            return ParentNode(f"h{header_type}",child_nodes_html_nodes, None)
        return LeafNode(f"h{header_type}", text)
    if type == "code":
        return ParentNode("pre",[ParentNode("code", child_nodes_html_nodes, None)], None)
    if type == "quote":
        return ParentNode("blockquote", child_nodes_html_nodes, None)
    if type == "ordered_list":
        return ParentNode("ol", [ParentNode("li", child_nodes_html_nodes, None)], None)
    if type == "unordered_list":
        return ParentNode("ul", [ParentNode("li", child_nodes_html_nodes, None)], None)
    if type == "paragraph":
        if len(child_nodes_html_nodes) > 0:
            return ParentNode(f"p",child_nodes_html_nodes, None)
        return LeafNode(f"p", text)

     
