import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
    Tag
)

class TestHTMLNode(unittest.TestCase):    
    def test_props_to_html(self):
        node = HTMLNode(Tag.LINK, "link", None, {"id": "title", "href": "https://test.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(),
            ' id="title" href="https://test.com" target="_blank"'
        )

    def test_repr(self):
        node = HTMLNode(Tag.HEADING1, "This is a heading", None, {"id": "title"})
        self.assertEqual(
            repr(node),
            "HTMLNode(tag: h1, value: This is a heading, children: None, props: {'id': 'title'})"
        )

    def test_repr_no_tag(self):
        node = HTMLNode(None, "This is a heading", None, {"id": "title"})
        self.assertEqual(
            repr(node),
            "HTMLNode(tag: None, value: This is a heading, children: None, props: {'id': 'title'})"
        )


class TestLeafNode(unittest.TestCase): 
    def test_leaf_node_to_html(self):
        leaf_node = LeafNode(Tag.LINK, "This is a leaf node", {"href": "https://test.com", "target": "_blank"})
        self.assertEqual(
            leaf_node.to_html(),
            '<a href="https://test.com" target="_blank">This is a leaf node</a>'
        )

    def test_leaf_node_to_html_no_tag(self):
        leaf_node = LeafNode(None, "This is another leaf node")
        self.assertEqual(
            leaf_node.to_html(),
            "This is another leaf node"
        )

    def test_leaf_node_repr(self):
        leaf_node = LeafNode(Tag.LINK, "This is a leaf node", {"href": "https://test.com", "target": "_blank"})
        self.assertEqual(
            repr(leaf_node),
            "LeafNode(tag: a, value: This is a leaf node, props: {'href': 'https://test.com', 'target': '_blank'})"
        )


class TestParentNode(unittest.TestCase):
    def test_parent_node_to_html_1(self):
        # Testing a parent node with only leaf nodes
        parent_node = ParentNode(
            Tag.PARAGRAPH,
            [
                LeafNode(None, "leaf node"),
                LeafNode(Tag.LINK, "This is a test", {"href": "https://test.com"})
            ],
            {"id": "title"}
        )
        self.assertEqual(
            parent_node.to_html(),
            '<p id="title">leaf node<a href="https://test.com">This is a test</a></p>'
        )

    def test_parent_node_to_html_2(self):
        # Testing a parent node with parent nodes and leaf nodes
        parent_node = ParentNode(
            Tag.DIV,
            [
                ParentNode(
                    Tag.PARAGRAPH,
                    [LeafNode(Tag.ITALIC, "This is a test of "), LeafNode(Tag.BOLD, "a leaf node")],
                    {"id": "first parent"}
                ),
                ParentNode(
                    Tag.PARAGRAPH,
                    [LeafNode(None, "and parent node")],
                    {"id": "second parent"}
                ),
                LeafNode(None, "This is the leaf node!")
            ],
            {"id": "main"}
        )
        self.assertEqual(
            parent_node.to_html(),
            '<div id="main"><p id="first parent"><i>This is a test of </i><b>a leaf node</b></p><p id="second parent">and parent node</p>This is the leaf node!</div>'
        )

    def test_parent_node_to_html_3(self):
        # Testing parent nodes in parent nodes in parent nodes
        parent_node = ParentNode(
            Tag.BODY,
            [
                ParentNode(
                    Tag.DIV,
                    [
                        ParentNode(
                            Tag.PARAGRAPH,
                            [LeafNode(None, "This is the leaf node!")],
                            {"id": "third parent"}
                        )
                    ],
                    {"id": "second parent"}
                )
            ],
            {"id": "first parent"}
        )
        self.assertEqual(
            parent_node.to_html(),
            '<body id="first parent"><div id="second parent"><p id="third parent">This is the leaf node!</p></div></body>'
        )

    
    def test_parent_node_repr(self):
        parent_node = ParentNode(
            Tag.PARAGRAPH,
            [
                LeafNode(None, "leaf node"),
                LeafNode(Tag.LINK, "This is a test", {"href": "https://test.com"})
            ],
            {"id": "title"}
        )
        self.assertEqual(
            repr(parent_node),
            "ParentNode(tag: p, children: [LeafNode(tag: None, value: leaf node, props: None), LeafNode(tag: a, value: This is a test, props: {'href': 'https://test.com'})], props: {'id': 'title'})"
        )


if __name__ == "__main__":
    unittest.main()