from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

import json
import os

BOOKS_IN_COL = 2
BOOKS_ON_PAGE = 20
PAGES_SHIFT = 5


def get_books_info(path='data/books_info.json'):
    with open(path) as f:
        books_info = json.loads(f.read())
    return books_info


def on_reload(template_path='template.html', render_path='index{page_number}.html', folder='pages'):
    books_info = get_books_info()

    books_pairs = list(chunked(books_info, BOOKS_IN_COL, strict=False))
    books_pages = list(chunked(books_pairs, BOOKS_ON_PAGE // BOOKS_IN_COL, strict=False))

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template(template_path)

    if folder:
        os.makedirs(folder, exist_ok=True)
        render_path = os.path.join(folder, render_path)

    for page, books_pairs in enumerate(books_pages):
        first_page = max((page + 1) - PAGES_SHIFT, 1)
        last_page = min((page + 1) + PAGES_SHIFT, len(books_pages))
        rendered_page = template.render(books_pairs=books_pairs, first_page=first_page, last_page=last_page,
                                        current_page=page + 1, global_last_page=len(books_pages))
        with open(render_path.format(page_number=page + 1), 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
