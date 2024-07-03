import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node
)

from htmlnode import (
    LeafNode,
    Tag
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false_type(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false_text(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is another text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_false_url(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.test.com")
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.test.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.test.com")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(repr(node), "TextNode(text: This is a text node, type: code, url: None)")

    # Test text_node_to_html_node(text_node)

    def test_textnode_to_html_node1(self):
        text_node = TextNode("This is a hippo", TextType.TEXT)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(
            repr(leaf_node),
            repr(LeafNode(Tag.NONE, "This is a hippo"))
        )

    def test_textnode_to_html_node2(self):
        text_node = TextNode("This is a link", TextType.LINK, "https://www.test.com")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(
            repr(leaf_node),
            repr(LeafNode(Tag.LINK, "This is a link", {"href": "https://www.test.com"}))
        )

    def test_textnode_to_html_node3(self):
        text_node = TextNode("This is a hippo", TextType.IMAGE, "hippo.jpg")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(
            repr(leaf_node),
            repr(LeafNode(Tag.IMAGE, "", {"src": "hippo.jpg", "alt": "This is a hippo"}))
        )


if __name__ == "__main__":
    unittest.main()