from htmlnode import (
    ParentNode,
    Tag
)

from textnode import (
    text_node_to_html_node
)

from inline_markdown import (
    text_to_textnodes
)

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        child = block_to_html_node(block, block_type)
        children.append(child)
    
    return ParentNode(Tag.DIV, children)

def markdown_to_blocks(markdown):
    blocks = []
    split_markdown = markdown.split("\n\n")
    
    for line in split_markdown:
        if line == "":      #don't want empty blocks
            continue
        blocks.append(line.strip())

    return blocks

def block_to_block_type(block):
    import functools
    block_lines = block.split("\n")
    
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```") and len(block_lines) > 1:
        return BlockType.CODE

    if len(block_lines) == functools.reduce(lambda x, y: x+1 if y.startswith(">") else x, block_lines, 0):
        return BlockType.QUOTE
   
    if len(block_lines) == functools.reduce(lambda x, y: x+1 if y.startswith("* ") else x, block_lines, 0):
        return BlockType.UNORDERED_LIST
    if len(block_lines) == functools.reduce(lambda x, y: x+1 if y.startswith("- ") else x, block_lines, 0):
        return BlockType.UNORDERED_LIST
    
    if len(block_lines) == functools.reduce(lambda x, y: x+1 if y.startswith(f"{x+1}. ") else x, block_lines, 0):
        return BlockType.ORDERED_LIST    
    
    return BlockType.PARAGRAPH

def block_to_html_node(block, block_type : BlockType):
    match block_type:
        case BlockType.HEADING:
            return block_to_heading_node(block)
        case BlockType.CODE:
            return block_to_code_node(block)
        case BlockType.QUOTE:
            return block_to_quote_node(block)
        case BlockType.UNORDERED_LIST:
            return block_to_unordered_list_node(block)
        case BlockType.ORDERED_LIST:
            return block_to_ordered_list_node(block)
        case BlockType.PARAGRAPH:
            return block_to_paragraph_node(block)
    
    raise ValueError(f"Invalid BlockType: {block_type}")

def block_to_heading_node(block):
    tag = Tag.NONE
    if block.startswith("# "):
        tag = Tag.HEADING1
        block = block.lstrip("# ")
    elif block.startswith("## "):
        tag = Tag.HEADING2
        block = block.lstrip("## ")
    elif block.startswith("### "):
        tag = Tag.HEADING3
        block = block.lstrip("### ")
    elif block.startswith("#### "):
        tag = Tag.HEADING4
        block = block.lstrip("#### ")
    elif block.startswith("##### "):
        tag = Tag.HEADING5
        block = block.lstrip("##### ")
    elif block.startswith("###### "):
        tag = Tag.HEADING6
        block = block.lstrip("###### ")
    else:
        raise ValueError("Invalid heading size")
    
    text_nodes = text_to_textnodes(block)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))

    return ParentNode(tag, children)

def block_to_code_node(block):
    block = block.strip("```")
    
    text_nodes = text_to_textnodes(block)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))

    code_child = ParentNode(Tag.CODE, children)
    return ParentNode(Tag.PRE, [code_child])

def block_to_quote_node(block):
    block = "\n".join(map(lambda line : line.lstrip(">").strip(), block.split("\n")))
    
    text_nodes = text_to_textnodes(block)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))

    return ParentNode(Tag.QUOTE, children)

def block_to_unordered_list_node(block):
    block = map(lambda line : line[2:], block.split("\n"))

    children = []
    
    for line in block:
        grand_children = []
        text_nodes = text_to_textnodes(line)
        for node in text_nodes:
            grand_children.append(text_node_to_html_node(node))
        children.append(ParentNode(Tag.LIST_ITEM, grand_children))

    return ParentNode(Tag.UNORDERED_LIST, children)

def block_to_ordered_list_node(block):
    block = map(lambda line : line[3:], block.split("\n"))
    children = []
    
    for line in block:
        grand_children = []
        text_nodes = text_to_textnodes(line)
        for node in text_nodes:
            grand_children.append(text_node_to_html_node(node))
        children.append(ParentNode(Tag.LIST_ITEM, grand_children))

    return ParentNode(Tag.ORDERED_LIST, children)

def block_to_paragraph_node(block):
    text_nodes = text_to_textnodes(block)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))

    return ParentNode(Tag.PARAGRAPH, children)