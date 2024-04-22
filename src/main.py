from textnode import TextNode
from htmlnode import *
from markdown_blocks import markdown_to_html_node
from gen import gen_func
import os, shutil

def main():

    def extract_title(md):
        output = []
        lines = md.split('\n\n')
        for line in lines:
            if line.strip()[:2] == '# ':
                output.append(line.strip()[2:])
        if len(output) == 0:
            raise Exception('Markdown has no header')
        return output[0]

    def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
        for content in os.listdir(path=dir_path_content):
            if os.path.isfile(f'{dir_path_content}/{content}'):
                index_file = f'{dir_path_content}/{content}'
                dest_file = f'{dest_dir_path}/index.html'
                generate_page(index_file, template_path, dest_file)
            else:
                new_dir = f'{dest_dir_path}/{content}'
                new_src = f'{dir_path_content}/{content}'
                os.mkdir(new_dir)
                generate_pages_recursive(new_src, template_path, new_dir)

    def generate_page(from_path, template_path, dest_path):
        print(f'Generating page from {from_path} to {dest_path} using {template_path}.')
        try:
            with open(from_path, 'r') as from_pa:
                markdown_file = from_pa.read()
                html_node = markdown_to_html_node(markdown_file).to_html()
            with open(template_path, 'r') as temp_path:
                template = temp_path.read()
                title = extract_title(markdown_file)
                output = template.replace('{{ Title }}', title)
                output = output.replace('{{ Content }}', html_node)
        except Exception as e:
            print('Problem reading files: --->' + f'{e}')



        check_path = ''
        for direc in dest_path.split('/'):
            #print(direc)
            pass

        try:
            html_file = dest_path
            with open(html_file, 'w') as file:
                file.write(output)
                print('SUCCES')
        except Exception as e:
            print(e)

    home = './static'
    destnation = './public'

    
    from_p = './content/index.md'
    use = './template.html'
    to_path = './public/index.html'

    content_dir = './content'
    dest_dir = './public'
    gen_func(home, destnation)
#    generate_page(from_p, use, to_path)
    generate_pages_recursive(content_dir, use, dest_dir)

if __name__ == '__main__':
    main()

