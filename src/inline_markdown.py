import re

from textnode import (
    TextNode,
    TextType
)


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    #bold & italic & code
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    #images & links
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type : TextType):
    #Always run this one for bold before you do italics, or else the bold will be messed up
    
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:     #Only TextType.TEXT nodes are to be split
            new_nodes.append(node)
            continue       
        
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError("Invalid markdown: formatted section not closed")
            
        texts = node.text.split(delimiter)

        #if the first char is not the delimiter, then it will be text
        will_be_text_type = not node.text.startswith(delimiter)

        for text in texts:
            if text == "":
                continue
                
            if will_be_text_type:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))
                
            will_be_text_type = not will_be_text_type
        
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        
        # if the TextType is not TEXT or there are no images in the TEXT node, just append the node
        if node.text_type != TextType.TEXT or not images:
            new_nodes.append(node)
            continue
        
        remaining_text = node.text

        for image_tup in images: #image_tup is a tuple of alt text and image url
            splits = remaining_text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)

            # if the first element has text, it becomes a Text node; if it is empty remaining_text starts with an image
            if splits[0] != "":
                new_nodes.append(TextNode(splits[0], TextType.TEXT))
            
            new_nodes.append(TextNode(image_tup[0], TextType.IMAGE, image_tup[1]))

            remaining_text = splits[1]

        #if the initial text had any text after the last image, it gets added here
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        
        # if the TextType is not TEXT or there are no images in the TEXT node, just append the node
        if node.text_type != TextType.TEXT or not links:
            new_nodes.append(node)
            continue
        
        remaining_text = node.text

        for link_tup in links: #link_tup is a tuple of link text and url
            splits = remaining_text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)

            # if the first element has text, it becomes a Text node; if it is empty remaining_text starts with an link
            if splits[0] != "":
                new_nodes.append(TextNode(splits[0], TextType.TEXT))
            
            new_nodes.append(TextNode(link_tup[0], TextType.LINK, link_tup[1]))

            remaining_text = splits[1]

        #if the initial text had any text after the last link, it gets added here
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text): 
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)