import unittest

from htmlnode import (
    HTMLNode,
    Tag
)

class TestHTMLNode(unittest.TestCase):    
    def test_props_to_html(self):
        node = HTMLNode(Tag.A, "link", None, {"id": "title", "href": "https://test.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(),
            ' id="title" href="https://test.com" target="_blank"'
        )

    def test_repr(self):
        node = HTMLNode(Tag.H1, "This is a heading", None, {"id": "title"})
        self.assertEqual(
            repr(node),
            "HTMLNode(tag: h1, value: This is a heading, children: None, props/attributes: {'id': 'title'})"
        )




if __name__ == "__main__":
    unittest.main()