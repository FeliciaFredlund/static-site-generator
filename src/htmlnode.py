from enum import Enum

class Tag(Enum):
    P = "p"
    DIV = "div"
    A = "a"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = Tag(tag)         # an enum for HTML tags
        self.value = value          # Content/value between opening and closing tag
        self.children = children    # A list of HTMLnode objects representing the children of this node
        self.props = props          # A dictionary holding the attributes of the tag, example {"href": "https://www.test.com"}

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        attributes = []
        for key, value in self.props.items():
            attributes.append(f' {key}="{value}"')
        return "".join(attributes)      # if self.props is None/empty, an empty string is sent
    
    def __repr__(self):
        return f"HTMLNode(tag: {self.tag.value}, value: {self.value}, children: {self.children}, props/attributes: {self.props})"
