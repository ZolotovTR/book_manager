def get_csv_from_str(string: str) -> str:
    """
    Парсил с сайта: https://infoselection.ru/infokatalog/literatura-knigi/literatura-obshchee/item/
    1001-100-luchshikh-proizvedenij-russkoj-literatury
    :param string: Строка для парсинга
    :return:
    """
    for line in string.split('\n'):
        i, title, author, year = line.split('\t')
        if '—' in year:
            year = year.split('—')[0]
        return f'{title},{author},{year}'
