from enum import Enum

class Tag(Enum):
    HEAD = "head"
    BODY = "body"
    DIV = "div"
    PARAGRAPH = "p"
    SPAN = "span"
    HEADING1 = "h1"
    HEADING2 = "h2"
    HEADING3 = "h3"
    LINK = "a"
    BOLD = "b"
    ITALIC = "i"
    NONE = None

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = Tag(tag)         # an enum for HTML tags
        self.value = value          # Content/value between opening and closing tag
        self.children = children    # A list of HTMLnode objects representing the children of this node
        self.props = props          # A dictionary holding the attributes of the tag, example {"href": "https://www.test.com"}

    def to_html(self):          #creates a string with correct HTML for all elements
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        string_props = []
        for key, value in self.props.items():       # changes each prop to a string (starting with a space) with correct HTML
            string_props.append(f' {key}="{value}"')
        return "".join(string_props)
    
    def __repr__(self):
        return f"HTMLNode(tag: {self.tag.value}, value: {self.value}, children: {self.children}, props: {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):          #creates a string with correct HTML for all elements
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        
        if self.tag.value is None:
            return self.value
        
        return f"<{self.tag.value}{self.props_to_html()}>{self.value}</{self.tag.value}>"

    def __repr__(self):
        return f"LeafNode(tag: {self.tag.value}, value: {self.value}, props: {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):          #creates a string with correct HTML for all elements
        if self.tag is Tag.NONE:
            raise ValueError("Invalid HTML: no tag")

        if self.children is None:
            raise ValueError("Invalid HTML: no children")
        
        strings_for_parent_and_children = []
        # Parent opening tag
        strings_for_parent_and_children.append(f"<{self.tag.value}{self.props_to_html()}>")
        
        # Adding all children strings
        for child in self.children:
            strings_for_parent_and_children.append(child.to_html())
        
        # Parent closing tag
        strings_for_parent_and_children.append(f"</{self.tag.value}>")

        return "".join(strings_for_parent_and_children)

    
    def __repr__(self):
        return f"ParentNode(tag: {self.tag.value}, children: {self.children}, props: {self.props})"