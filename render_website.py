import glob
import json
import os
import pathlib

from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked
from livereload import Server

BOOKS_IN_COL = 2
BOOKS_ON_PAGE = 20
PAGES_SHIFT = 5


def get_books(path='data/books_info.json'):
    with open(path) as f:
        books = json.loads(f.read())
    return books


def clean_data(books, folder='data', formats=('txt', 'jpg', 'gif')):
    current_files = []
    for format in formats:
        current_files += glob.glob(f'{folder}/**/*.{format}', recursive=True)

    books_txt_files = [book['book_path'] for book in books]
    books_img_files = [book['image_src'] for book in books]

    current_files = set(current_files)
    need_files = set(books_txt_files + books_img_files)

    current_files = {pathlib.Path(file) for file in current_files}
    need_files = {pathlib.Path(file) for file in need_files}

    extra_files = current_files.difference(need_files)

    for file in extra_files:
        os.remove(file)


def on_reload(template_path='template.html', render_path='index{page_number}.html', folder='pages'):
    books = get_books()

    clean_data(books)

    books_pairs = list(chunked(books, BOOKS_IN_COL, strict=False))
    books_pages = list(chunked(books_pairs, BOOKS_ON_PAGE // BOOKS_IN_COL, strict=False))

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template(template_path)

    os.makedirs(folder, exist_ok=True)
    render_path = os.path.join(folder, render_path)

    for page in os.listdir(folder):
        os.remove(os.path.join(folder, page))

    for page, books_pairs in enumerate(books_pages, start=1):
        first_page = max(page - PAGES_SHIFT, 1)
        last_page = min(page + PAGES_SHIFT, len(books_pages))
        rendered_page = template.render(books_pairs=books_pairs, first_page=first_page, last_page=last_page,
                                        current_page=page, global_last_page=len(books_pages))
        with open(render_path.format(page_number=page), 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
