from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

import json


def get_books_info(path='data/books_info.json'):
    with open(path) as f:
        books_info = json.loads(f.read())
    return books_info


def on_reload(template_path='template.html', render_path='index.html'):
    books_info = get_books_info()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template(template_path)

    rendered_page = template.render(books=books_info)

    with open(render_path, 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == '__main__':
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
