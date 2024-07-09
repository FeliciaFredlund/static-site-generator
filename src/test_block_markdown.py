import unittest

from block_markdown import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    block_to_html_node,
    BlockType
)

from htmlnode import (
    LeafNode,
    ParentNode,
    Tag
)

class TestBlockMarkdown(unittest.TestCase):
    def test_mardown_to_blocks_multiline_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"
            ]
        )
    
    def test_markdown_to_blocks_stripping_whitespace(self):
        markdown = """This is **bolded** paragraph




        This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line   

   * This is a list
* with items   
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"
            ]
        )


    def test_block_to_block_type_heading(self):
        block = "## Heading"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )

        block = "####### Heading too small"         #heading only goes 6 deep
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_code(self):
        block = "```This is code\nAnd more code on a new line```"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.CODE
        )

        # Missing 2 ticks at the end
        block = "```This is code\nAnd more code on a new line`"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )

        # Only a single line of code, so it is inline code rather than a block
        block = "```This is code. And no extra lines so not a block code apparently```"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_quote(self):
        block = ">This is a blockquote\n>With more than one line\n>3 lines to be exact"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.QUOTE
        )

        block = ">This is a blockquote\nThis line should have a quote marker but we forgot\n>3 lines to be exact"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_unordered_star(self):
        block = "* This is an unordered list\n* Only starting with star\n* And one more element for consistency"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.UNORDERED_LIST
        )

        block = "* This is an unordered list\n* Starting with star\n- Except here we switched so this is maybe not a list"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_ordered(self):
        block = "1. This is an ordered list\n2. With three items\n3. Yep, three indeed"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.ORDERED_LIST
        )

        block = "1. This is an ordered list\n3. With three items\n3. But we numbered the second item incorrectly!!!"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_paragraph(self):
        block = "This is just a paragraph of text for generic testing of paragraph."
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )


    def test_block_to_html_node_heading(self):
        block = "# This is a Heading"
        node = block_to_html_node(block, BlockType.HEADING)
        self.assertEqual(
            repr(node),
            "ParentNode(tag: h1, children: [LeafNode(tag: None, value: This is a Heading, props: None)], props: None)"
        )

    def test_block_to_html_node_heading_with_italics(self):
        block = "# This is a *Heading*"
        node = block_to_html_node(block, BlockType.HEADING)
        self.assertEqual(
            repr(node),
            "ParentNode(tag: h1, children: [LeafNode(tag: None, value: This is a , props: None), LeafNode(tag: i, value: Heading, props: None)], props: None)"
        )

    def test_block_to_html_node_code(self):
        block = "```This is a code block.\nIs this right?```"
        node = block_to_html_node(block, BlockType.CODE)
        self.assertEqual(
            repr(node),
            "ParentNode(tag: pre, children: [ParentNode(tag: code, children: [LeafNode(tag: None, value: This is a code block.\nIs this right?, props: None)], props: None)], props: None)"
        )
    
    def test_block_to_html_node_quote(self):
        block = ">This is a quote block.\n>Is this right?"
        node = block_to_html_node(block, BlockType.QUOTE)
        self.assertEqual(
            repr(node),
            "ParentNode(tag: blockquote, children: [LeafNode(tag: None, value: This is a quote block.\nIs this right?, props: None)], props: None)"
        )

    def test_block_to_html_node_unordered_list_to_html_string_with_star(self):
        block = "* Item 1\n* Item 2\n* Item 3"
        node = block_to_html_node(block, BlockType.UNORDERED_LIST)
        correct_node = ParentNode(
            Tag.UNORDERED_LIST, 
            [
                ParentNode(Tag.LIST_ITEM, [LeafNode(Tag.NONE, "Item 1")]),
                ParentNode(Tag.LIST_ITEM, [LeafNode(Tag.NONE, "Item 2")]),
                ParentNode(Tag.LIST_ITEM, [LeafNode(Tag.NONE, "Item 3")])
            ]
        )
        self.assertEqual(
            node.to_html(),
            correct_node.to_html()
        )

    def test_block_to_html_node_unordered_list_to_html_string_with_hyphen(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        node = block_to_html_node(block, BlockType.UNORDERED_LIST)
        correct_node = ParentNode(
            Tag.UNORDERED_LIST, 
            [
                ParentNode(Tag.LIST_ITEM, [LeafNode(Tag.NONE, "Item 1")]),
                ParentNode(Tag.LIST_ITEM, [LeafNode(Tag.NONE, "Item 2")]),
                ParentNode(Tag.LIST_ITEM, [LeafNode(Tag.NONE, "Item 3")])
            ]
        )
        self.assertEqual(
            node.to_html(),
            correct_node.to_html()
        )
    
    def test_block_to_html_node_ordered_list_to_html(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        node = block_to_html_node(block, BlockType.ORDERED_LIST)
        correct_node = ParentNode(
            Tag.ORDERED_LIST, 
            [
                ParentNode(Tag.LIST_ITEM, [LeafNode(Tag.NONE, "Item 1")]),
                ParentNode(Tag.LIST_ITEM, [LeafNode(Tag.NONE, "Item 2")]),
                ParentNode(Tag.LIST_ITEM, [LeafNode(Tag.NONE, "Item 3")])
            ]
        )
        self.assertEqual(
            node.to_html(),
            correct_node.to_html()
        )

    def test_block_to_html_node_paragraph(self):
        block = "This is a paragraph block.\nWith more than one line. And some **bold** and *italics.*"
        node = block_to_html_node(block, BlockType.PARAGRAPH)
        correct_node = ParentNode(
            Tag.PARAGRAPH,
            [
                LeafNode(Tag.NONE, "This is a paragraph block.\nWith more than one line. And some "),
                LeafNode(Tag.BOLD, "bold"),
                LeafNode(Tag.NONE, " and "),
                LeafNode(Tag.ITALIC, "italics.")
            ]
        )
        self.assertEqual(
            repr(node),
            repr(correct_node)
        )


    def test_markdown_to_html_node_to_html(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        node = markdown_to_html_node(markdown)
        correct_node = ParentNode(
            Tag.DIV,
            [
                ParentNode(
                    Tag.PARAGRAPH,
                    [
                        LeafNode(Tag.NONE, "This is "),
                        LeafNode(Tag.BOLD, "bolded"),
                        LeafNode(Tag.NONE, " paragraph")
                    ]
                ),
                ParentNode(
                    Tag.PARAGRAPH,
                    [
                        LeafNode(Tag.NONE, "This is another paragraph with "),
                        LeafNode(Tag.ITALIC, "italic"),
                        LeafNode(Tag.NONE, " text and "),
                        LeafNode(Tag.CODE, "code"),
                        LeafNode(Tag.NONE, " here\nThis is the same paragraph on a new line")
                    ]
                ),
                ParentNode(
                    Tag.UNORDERED_LIST,
                    [
                        LeafNode(Tag.LIST_ITEM, "This is a list"),
                        LeafNode(Tag.LIST_ITEM, "with items")
                    ]
                )
            ]
        )
        self.assertEqual(
            node.to_html(),
            correct_node.to_html()
        )


if __name__ == "__main__":
    unittest.main()