import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


def extract_markdown_images(str):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    output = re.findall(pattern, str)
    return output

def extract_markdown_links(str):
    pattern = r"\[(.*?)\]\((.*?)\)"
    output = re.findall(pattern, str)
    return output


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    output = []
    types = {
        "**": "bold",
        "*": "italic",
        "`": "code"
    }
    for i in old_nodes:
        if i.text_type != text_type_text:
            output.append(i)
            continue
        nodes = i.text.split(delimiter)
        if len(nodes) % 2 == 0:
            raise Exception("Invalid Markdown syntax. Not closed delimiter")
        for j in range(len(nodes)):
            if nodes[j] == "":
                continue
            if (j+1)%2 == 0:
                output.append(TextNode(nodes[j], types[delimiter]))
            else:
                output.append(TextNode(nodes[j], "text"))
    return output

def split_nodes_image(old_nodes):
    output = []
    pattern = r"!\[(.*?)\]\((.*?)\)"
    # Each i in this loop is a text node
    for i in old_nodes:
        # If in that text node text content the regex returns True then extract nodes
        if re.search(pattern, i.text):
            tupe = extract_markdown_images(i.text)
            txt = re.split(pattern, i.text)
            for j in range(len(txt)):
                found = False
                for tup in tupe:
                    if txt[j] == tup[0] and txt[j+1] == tup[1]:
                        output.append(TextNode(tup[0], text_type_image, tup[1]))
                        found = True
                        continue
                    elif txt[j] == tup[0] or txt[j] == tup[1]:
                        found = True
                        continue 
                if found:
                    continue
                if not found and txt[j] != '':
                    output.append(TextNode(txt[j], text_type_text))
                
        # Else just append current node
        else:
            output.append(i)
    return output



def split_nodes_link(old_nodes):
    output = []
    pattern = r"\[(.*?)\]\((.*?)\)"
    # Each i in this loop is a text node
    for i in old_nodes:
        # If in that text node text content the regex returns True then extract nodes
        if re.search(pattern, i.text):
            tupe = extract_markdown_links(i.text)
            txt = re.split(pattern, i.text)
            for j in range(len(txt)):
                found = False
                for tup in tupe:
                    if txt[j] == tup[0] and txt[j+1] == tup[1]:
                        output.append(TextNode(tup[0], text_type_link, tup[1]))
                        found = True
                        continue
                    elif txt[j] == tup[0] or txt[j] == tup[1]:
                        found = True
                        continue 
                if found:
                    continue
                if not found and txt[j] != '':
                    output.append(TextNode(txt[j], text_type_text))
                
        # Else just append current node
        else:
            output.append(i)
    return output

def text_to_textnodes(str):
    output = [TextNode(str, text_type_text)]
    output = split_nodes_delimiter(output, "**", text_type_bold)
    output = split_nodes_delimiter(output, "*", text_type_bold)
    output = split_nodes_delimiter(output, "`", text_type_code)
    output = split_nodes_image(output)
    output = split_nodes_link(output)
    return output





