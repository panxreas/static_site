from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"

def markdown_to_blocks(markdown):
    unfiltered = markdown.split("\n\n")
    output = []
    for i in unfiltered:    
        if i != '':
            output.append(i.strip('\n'))
    return output

def block_to_block_type(block):
    lines = block.split('\n')
    if (
        block.startswith('# ')
        or block.startswith('## ')
        or block.startswith('### ')
        or block.startswith('#### ')
        or block.startswith('##### ')
        or block.startswith('###### ')
    ):
        return block_type_heading
    
    elif block[:3] == '```' and block[-3:] == '```':
        return block_type_code
    
    elif block[0] == '>':
        for line in lines:
            if not line.startswith('>'):
                return block_type_paragraph
        return block_type_quote
    
    elif block.startswith('* '):
        for line in lines:
            if not line.startswith('* '):
                return block_type_paragraph
        return block_type_ulist
    
    elif block.startswith('- '):
        for line in lines:
            if not line.startswith('- '):
                return block_type_paragraph
        return block_type_ulist

    elif block.startswith('1. '):
        count = 1
        for line in lines:
            if not line.startswith(f'{count}. '):
                return block_type_paragraph 
            count += 1
        return block_type_olist
    
    else:
        return block_type_paragraph

### --------------------- CONVERTORS

def to_paragraph(block):
    text_nodes = text_to_textnodes(block.replace('\n', ' '))
    children = []
    for i in text_nodes:
       children.append(text_node_to_html_node(i))
    return ParentNode('p',children)

def to_heading(block):
    no = block[:6].count('#')
    text_nodes = text_to_textnodes(block[no+1:])
    children = []
    for i in text_nodes:
       children.append(text_node_to_html_node(i))
    return ParentNode(f'h{no}',children)

def to_code(block):
    text_nodes = text_to_textnodes(block)
    children = []
    for i in text_nodes:
       children.append(text_node_to_html_node(i))
    return ParentNode('pre',children)

def to_quote(block):
    lines = block.split('\n')
    output = ''
    children = []
    for line in lines:
        output += line.lstrip('> ') + " "
    text_nodes = text_to_textnodes(output.rstrip())
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return ParentNode('blockquote', children)

def to_ulist(block):
    lines = block.split('\n')
    children = []
    for line in lines:
        nodes = text_to_textnodes(line[2:])
        child = []
        for node in nodes:
            html = text_node_to_html_node(node)
            child.append(html)
        children.append(ParentNode('li', child))
    return ParentNode('ul', children)

def to_olist(block):
    lines = block.split('\n')
    children = []
    for line in lines:
        nodes = text_to_textnodes(line[3:])
        child = []
        for node in nodes:
            html = text_node_to_html_node(node)
            child.append(html)
        children.append(ParentNode('li', child))
    return ParentNode('ol', children)

### --------------------- MARKDOWN TO HTML

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        if block_to_block_type(block) == 'paragraph':
            children.append(to_paragraph(block)) 
        elif block_to_block_type(block) == 'heading':
            children.append(to_heading(block))
        elif block_to_block_type(block) == 'code':
            children.append(to_code(block))
        elif block_to_block_type(block) == 'quote':
            children.append(to_quote(block))
        elif block_to_block_type(block) == 'unordered_list':
            children.append(to_ulist(block))
        elif block_to_block_type(block) == 'ordered_list':
            children.append(to_olist(block))

    return ParentNode('div', children)

