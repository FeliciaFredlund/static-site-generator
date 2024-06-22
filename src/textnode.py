text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text            # text content of the node
        self.text_type = text_type  # a string like "bold" or "italic"
        self.url = url              # url of a link or image
    
    def __eq__(self, other):
        # Only equal if all values match
        return (
            self.text == other.text 
            and self.text_type == other.text_type 
            and self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode(text: {self.text}, type: {self.text_type}, url: {self.url})"