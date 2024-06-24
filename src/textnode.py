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
        self.text_type = TextType(text_type)    # an enum for text types
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