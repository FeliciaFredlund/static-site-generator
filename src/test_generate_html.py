import unittest

from generate_html import (
    extract_title
)

class TestGenerateHTML(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
#    This is a H1 heading

And this is just some other text with some **bold** and `code`

>And a block quote just for fun
>That is two lines long"""
        title = extract_title(markdown)
        self.assertEqual(
            title,
            "This is a H1 heading"
        )
    
    def test_extract_title_no_title(self):
        markdown = """
## This is a H2 heading

And this is just some other text with some **bold** and `code`

>And a block quote just for fun
>That is two lines long"""
        with self.assertRaises(ValueError):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()