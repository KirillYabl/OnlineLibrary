from jinja2 import Environment, FileSystemLoader, select_autoescape

import json


def get_books_info(path='data/books_info.json'):
    with open(path) as f:
        books_info = json.loads(f.read())
    return books_info


if __name__ == '__main__':
    books_info = get_books_info()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(books=books_info)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
