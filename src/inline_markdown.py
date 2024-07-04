from textnode import (
    TextNode,
    TextType
)


def split_nodes_delimiter(old_nodes, delimiter, text_type : TextType):
    #Always run this one for bold before you do italics, or else the bold will be messed up
    
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:     #Only TextType.TEXT nodes are to be split
            new_nodes.append(node)       
        else:
            if node.text.count(delimiter) % 2 != 0:
                raise ValueError("Invalid markdown: formatted section not closed")
            
            texts = node.text.split(delimiter)

            #if the first char is not the delimiter, then it will be text
            will_be_text_type = node.text[0] is not delimiter

            for text in texts:
                if text == "":
                    continue
                
                if will_be_text_type:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text, text_type))
                
                will_be_text_type = not will_be_text_type
        
    return new_nodes