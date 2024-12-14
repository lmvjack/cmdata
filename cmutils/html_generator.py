# functions to manage html file generation
from jinja2 import Environment, FileSystemLoader
import os

def create_html(cards_info: list, filename: str):
    if not cards_info:
        print("No cards info downloaded, can't create html file.")
        return

    env = Environment(loader=FileSystemLoader('./templates'))

    # load the `index.jinja` template
    index_template = env.get_template('index.jinja')
    output_from_parsed_template = index_template.render(cards=cards_info)


    print("Creating html file...")

    folder: str = 'downloads'
    if not os.path.exists(folder):
        os.makedirs(folder)

    fullpath: str = os.path.join(folder, filename)

    with open(fullpath, 'w') as html_file:
        html_file.write(output_from_parsed_template)

    absolute_path = os.path.abspath(fullpath)
    print("Copy this path and paste it in your browser to open the file:")
    print(f"\033[91m\033[107m{absolute_path}\033[0m")