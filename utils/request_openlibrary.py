import requests
import csv

from typing import Any

PAGES_LIMIT = 10


def get_books(page_request: int) -> Any:
    url = f'https://openlibrary.org/subjects/russian_literature.json?limit=100&page={page_request}'
    response = requests.get(url)
    data = response.json()
    return data['works']


# Функция для сохранения данных в CSV-файле
def save_to_csv(data_for_save: Any) -> None:
    with open('books.csv', 'w', newline="", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Author', 'Year'])

        for book in data_for_save:
            title = book['title']
            author = book['authors'][0]['name'] if 'authors' in book else 'Unknown'
            year = book['first_publish_year']
            if 'о' in title or 'а' in title or 'е' in title or 'и' in title:
                writer.writerow([title, author, year])


def parse_all_pages() -> None:
    """
    Скачивание данных из API
    """
    page = 1
    books = []
    while page < PAGES_LIMIT:
        data = get_books(page)
        if not data:
            break
        books.extend(data)
        page += 1

    save_to_csv(books)

