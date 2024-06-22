import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)

    def test_eq_false_type(self):
        node = TextNode("This is a text node", text_type_image)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_false_text(self):
        node = TextNode("This is a text node", text_type_italic)
        node2 = TextNode("This is another text node", text_type_italic)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_link, "https://www.test.com")
        node2 = TextNode("This is a text node", text_type_link, "https://www.test.com")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_code)
        self.assertEqual(repr(node), "TextNode(This is a text node, code, None)")


if __name__ == "__main__":
    unittest.main()