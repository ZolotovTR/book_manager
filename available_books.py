import csv

AVAIBLE_BOOKS_FILE = 'available_books.csv'


def get_plain_titile(title: str) -> str:
    """

    :param title:
    :return:
    """
    plain_title = ''
    for char in title.lower():
        if char.isalpha():
            plain_title += char
    return plain_title


def get_dict_available_book(file_path: str) -> dict:
    name_to_book_mapping = dict()
    with open(file_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            name_to_book_mapping[get_plain_titile(row[0])] = row

    return name_to_book_mapping


all_available_books = get_dict_available_book(AVAIBLE_BOOKS_FILE)

