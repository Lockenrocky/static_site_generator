from textnode import TextNode, TEXTTYPE
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TEXTTYPE.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TEXTTYPE.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TEXTTYPE.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        matches_alt = re.finditer(r"(!\[(.*?)\])(\((.*?)\))", old_node.text)
        pos = 0
        for match in matches_alt:
            if not match.regs[0][0] == pos:
                split_nodes.append(TextNode(old_node.text[pos:match.regs[0][0]], TEXTTYPE.TEXT))
            split_nodes.append(TextNode(old_node.text[match.regs[2][0]:match.regs[2][1]], TEXTTYPE.IMAGE, old_node.text[match.regs[4][0]:match.regs[4][1]]))
            pos = match.regs[0][1]
        if pos < len(old_node.text):
            split_nodes.append(TextNode(old_node.text[pos:], TEXTTYPE.TEXT))            
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TEXTTYPE.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        matches_alt = re.finditer(r"(\[(.*?)\])(\((.*?)\))", old_node.text)
        pos = 0
        for match in matches_alt:
            if not match.regs[0][0] == pos:
                split_nodes.append(TextNode(old_node.text[pos:match.regs[0][0]], TEXTTYPE.TEXT))
            split_nodes.append(TextNode(old_node.text[match.regs[2][0]:match.regs[2][1]], TEXTTYPE.LINK, old_node.text[match.regs[4][0]:match.regs[4][1]]))
            pos = match.regs[0][1]
        if pos < len(old_node.text):
            split_nodes.append(TextNode(old_node.text[pos:], TEXTTYPE.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TEXTTYPE.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TEXTTYPE.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TEXTTYPE.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TEXTTYPE.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes    

def extract_markdown_images(text):
    matches_alt = re.findall(r"\[(.*?)\]", text)
    matches_url = re.findall(r"\((.*?)\)", text)
    list_of_tuples = []
    for i in range(0,len(matches_alt),1):
        list_of_tuples.append((matches_alt[i], matches_url[i]))
    return list_of_tuples

def extract_markdown_links(text):
    matches_link = re.findall(r"\[(.*?)\]", text)
    matches_url = re.findall(r"\((.*?)\)", text)
    list_of_tuples = []
    for i in range(0,len(matches_link),1):
        list_of_tuples.append((matches_link[i], matches_url[i]))
    return list_of_tuples