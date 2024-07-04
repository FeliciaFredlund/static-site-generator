import unittest

from inline_markdown import (
    split_nodes_delimiter
)

from textnode import (
    TextNode,
    TextType
)


class TestInlineMarkdown(unittest.TestCase):

    def test_split_node_delimiter_bold(self):
        old_node = TextNode("This *is* **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([old_node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This *is* ", TextType.TEXT), 
                TextNode("bold", TextType.BOLD)
            ]
        )


    def test_split_node_delimiter_code_double(self):
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

    def test_split_node_delimiter_two_nodes(self):
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

    def test_split_node_delimiter_first_element_is_code_and_extra_non_text_node(self):
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
    
    def test_split_node_delimiter_incorrect_markdown(self):
        old_node = TextNode("This is **bold.", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([old_node], "**", TextType.BOLD)


if __name__ == "__main__":
    unittest.main()