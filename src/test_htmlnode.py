import unittest

from htmlnode import (
    HTMLNode,
    tag_a,
    tag_p,
    tag_h1,
    tag_h2,
    tag_h3,
    tag_div
)

class TestHTMLNode(unittest.TestCase):    
    def test_props_to_html(self):
        node = HTMLNode(tag_a, "link", None, {"id": "title", "href": "https://test.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(),
            ' id="title" href="https://test.com" target="_blank"'
        )

    def test_repr(self):
        node = HTMLNode(tag_h1, "This is a heading", None, {"id": "title"})
        self.assertEqual(
            repr(node),
            "HTMLNode(tag: h1, value: This is a heading, children: None, props/attributes: {'id': 'title'})"
        )




if __name__ == "__main__":
    unittest.main()