from htmlnode import (
    LeafNode,
    Tag
)

from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text                        # text content of the node
        
        self.text_type = None                   # an enum for text types    
        if text_type in TextType.__members__.values():                                    
            self.text_type = TextType(text_type)   
        else:
            raise ValueError(f"Invalid text_type: {text_type}")
        
        self.url = url                          # url of a link or image
    
    def __eq__(self, other):
        # Only equal if all values match
        return (
            self.text == other.text 
            and self.text_type == other.text_type 
            and self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode(text: {self.text}, type: {self.text_type.value}, url: {self.url})"


def text_node_to_html_node(text_node : TextNode):
    tag = Tag.NONE
    props = None
    
    match text_node.text_type:      # TextType.TEXT would be Tag.NONE so no need to have a case for it
        case TextType.BOLD:
            tag = Tag.BOLD
        case TextType.ITALIC:
            tag = Tag.ITALIC
        case TextType.CODE:
            tag = Tag.CODE
        case TextType.LINK:
            tag = Tag.LINK
            props = {"href": text_node.url}
        case TextType.IMAGE:
            tag = Tag.IMAGE
            props = {"src": text_node.url, "alt": text_node.text}
            text_node.text = ""

    return LeafNode(tag, text_node.text, props)