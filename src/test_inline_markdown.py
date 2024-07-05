import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link
)

from textnode import (
    TextNode,
    TextType
)


class TestInlineMarkdown(unittest.TestCase):

    def test_split_nodes_delimiter_bold(self):
        old_node = TextNode("This *is* **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([old_node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This *is* ", TextType.TEXT), 
                TextNode("bold", TextType.BOLD)
            ]
        )

    def test_split_nodes_delimiter_code_double(self):
        old_node = TextNode("This is `code and` this is also `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([old_node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT), 
                TextNode("code and", TextType.CODE), 
                TextNode(" this is also ", TextType.TEXT), 
                TextNode("code", TextType.CODE)
            ]
        )

    def test_split_nodes_delimiter_two_nodes(self):
        old_nodes = [TextNode("This is *italics*!", TextType.TEXT), TextNode("This is *italics*!", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT), 
                TextNode("italics", TextType.ITALIC),
                TextNode("!", TextType.TEXT),
                TextNode("This is ", TextType.TEXT), 
                TextNode("italics", TextType.ITALIC),
                TextNode("!", TextType.TEXT)
            ]
            
        )

    def test_split_nodes_delimiter_first_element_is_code_and_extra_non_text_node(self):
        old_nodes = [TextNode("`This is` code.", TextType.TEXT), TextNode("This is *italics*!", TextType.ITALIC)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is", TextType.CODE), 
                TextNode(" code.", TextType.TEXT), 
                TextNode("This is *italics*!", TextType.ITALIC)
            ]
        )
    
    def test_split_nodes_delimiter_incorrect_markdown(self):
        old_node = TextNode("This is **bold.", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([old_node], "**", TextType.BOLD)


    def test_extract_markdown_image(self):
        image = extract_markdown_images("See this monkey: ![monkey eating banana](monkey.jpg)")
        self.assertListEqual(
            image,
            [("monkey eating banana", "monkey.jpg")]
        )

    def test_extract_markdown_multiple_images(self):
        image = extract_markdown_images("![sleeping cat](cat1.jpg)<-- See my cat -->![sitting cat](cat2.jpg)")
        self.assertListEqual(
            image,
            [("sleeping cat", "cat1.jpg"), ("sitting cat", "cat2.jpg")]
        )

    def test_extract_markdown_link(self):
        link = extract_markdown_links("This is a [link](link.com).")
        self.assertListEqual(
            link,
            [("link", "link.com")]
        )

    def test_extract_markdown_multiple_links(self):
        links = extract_markdown_links("This is a [link](link.com) and also [this](this.com).")
        self.assertListEqual(
            links,
            [("link", "link.com"), ("this", "this.com")]
        )

    def test_extract_markdown_link_and_image(self):
        text = "[Wikipedia](wikipedia.com) says that this monkey is silly: ![silly monkey](monkey.jpg)"
        link = extract_markdown_links(text)
        image = extract_markdown_images(text)
        link_and_image = link + image
        self.assertListEqual(
            link_and_image,
            [("Wikipedia", "wikipedia.com"), ("silly monkey", "monkey.jpg")]
        )


    def test_split_nodes_image(self):
        old_nodes = [
            TextNode("This monkey is silly: ![silly monkey](monkey.jpg)", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This monkey is silly: ", TextType.TEXT),
                TextNode("silly monkey", TextType.IMAGE, "monkey.jpg")
            ]
        )
    
    def test_split_nodes_images(self):
        old_nodes = [
            TextNode("![first an image](some.jpg) This monkey is silly: ![silly monkey](monkey.jpg)", TextType.TEXT),
            TextNode("Some text and then ![an image](image.jpg) and then more text", TextType.TEXT),
            TextNode("This is some code and should not be touched", TextType.CODE),
            TextNode("Just a text node with no images but a [link](link.com)", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("first an image", TextType.IMAGE, "some.jpg"),
                TextNode(" This monkey is silly: ", TextType.TEXT),
                TextNode("silly monkey", TextType.IMAGE, "monkey.jpg"),
                TextNode("Some text and then ", TextType.TEXT),
                TextNode("an image", TextType.IMAGE, "image.jpg"),
                TextNode(" and then more text", TextType.TEXT),
                TextNode("This is some code and should not be touched", TextType.CODE),
                TextNode("Just a text node with no images but a [link](link.com)", TextType.TEXT)
            ]
        )


    def test_split_nodes_link(self):
        old_nodes = [
            TextNode("This [silly monkey](monkey.com) is my friend", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This ", TextType.TEXT),
                TextNode("silly monkey", TextType.LINK, "monkey.com"),
                TextNode(" is my friend", TextType.TEXT)
            ]
        )  
    
    def test_split_nodes_links(self):
        old_nodes = [
            TextNode("[first a link](some.com) This monkey is silly: [silly monkey](monkey.com)", TextType.TEXT),
            TextNode("Some text and then [a link](link.com) and then more text", TextType.TEXT),
            TextNode("This is some code and should not be touched", TextType.CODE),
            TextNode("Just a text node with no links but an ![image](image.jpg)", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("first a link", TextType.LINK, "some.com"),
                TextNode(" This monkey is silly: ", TextType.TEXT),
                TextNode("silly monkey", TextType.LINK, "monkey.com"),
                TextNode("Some text and then ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "link.com"),
                TextNode(" and then more text", TextType.TEXT),
                TextNode("This is some code and should not be touched", TextType.CODE),
                TextNode("Just a text node with no links but an ![image](image.jpg)", TextType.TEXT)
            ]
        )


if __name__ == "__main__":
    unittest.main()