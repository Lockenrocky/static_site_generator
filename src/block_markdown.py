import re

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
    if re.search("^```\n.*\n```$", md_block):
        return block_type_code
    if re.search("^>", md_block):
        return block_type_quote
    if re.search("^[*-] .*", md_block):
        return block_type_ulist
    if re.search("^[1-9]. .*", md_block):
        return block_type_olist
    return block_type_paragraph

     
