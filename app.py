from PyQt5.QtWidgets import (
    QVBoxLayout, QLabel, QPushButton, QWidget, QGridLayout, QApplication, QDesktopWidget, QInputDialog, QGroupBox,
    QBoxLayout
)
from PyQt5.QtCore import Qt
from available_books import get_plain_titile, all_available_books

from typing import Callable, Optional

APPLICATION_TITLE = 'Book Manager'

MAIN_WINDOW_WIDTH = 1200
MAIN_WINDOW_HEIGHT = 800

MAX_BOX_HEIGHT = 200

ADD_BOOK_MESSAGE = 'Добавить книгу'
ADD_BOOK_BUTTON_CFG = 'color: darkgreen;'

EDIT_MESSAGE = 'Редактировать'
EDIT_BOOK_BUTTON_CFG = 'color: orange;'

DELETE_MESSAGE = 'Удалить'
DELETE_BUTTON_CFG = 'color: darkred;'

ENTER_BOOK_NAME = 'Название книги:'
ENTER_AUTHOR_NAME = 'Автор книги:'
ENTER_YEAR_OF_BOOK = 'Введите год книги:'

BOOK_CONFIG = [
    ('Собираюсь читать', 'Приостановил чтение'),
    ('Сейчас читаю', 'Начать читать'),
    ('Прочитанные книги', 'Дочитал книгу'),
]

BOOK_STATUS = [status_config[0] for status_config in BOOK_CONFIG]
BOOK_ANSWER = [status_config[1] for status_config in BOOK_CONFIG]
STATUS_COUNTS = len(BOOK_CONFIG)


class BookBox(QGroupBox):
    def __init__(
            self,
            book_name: str,
            author: str,
            year: Optional[int],
            status_id: int,
            main_update: Callable,
            main_layout
    ) -> None:
        """
        Box каждой книги с полями, каждый бокс принадлежит одному из статусов
        :param book_name: имя книги
        :param author: автор произведения
        :param year: год первой публикации
        :param status_id: номер колонки стастусов
        :param main_update: функция обновления всех ввиджетов
        :param main_layout: Слои основного виждета
        """
        super().__init__(author)
        self.book_name = book_name
        self.author = author
        self.year = year

        self.status_id = status_id
        self.main_update = main_update

        self.layout = QVBoxLayout()
        self.main_layout = main_layout
        self.setMaximumHeight(MAX_BOX_HEIGHT)

        title = QLabel(book_name)
        self.layout.addWidget(title)
        if year:
            book_year = QLabel(str(year))
            self.layout.addWidget(book_year)

        if self.status_id > 0:
            self.left_button = QPushButton(BOOK_ANSWER[self.status_id - 1])
            self.layout.addWidget(self.left_button)
            self.left_button.clicked.connect(self.to_left_book, self.status_id)

        if self.status_id < STATUS_COUNTS - 1:
            self.right_button = QPushButton(BOOK_ANSWER[self.status_id + 1])
            self.layout.addWidget(self.right_button)
            self.right_button.clicked.connect(self.to_right_book, self.status_id)

        self.edit_button = QPushButton(EDIT_MESSAGE)
        self.edit_button.setStyleSheet(EDIT_BOOK_BUTTON_CFG)
        self.layout.addWidget(self.edit_button)
        self.edit_button.clicked.connect(self.edit_book, self.status_id)

        self.delete_button = QPushButton(DELETE_MESSAGE)
        self.delete_button.setStyleSheet(DELETE_BUTTON_CFG)
        self.layout.addWidget(self.delete_button)
        self.delete_button.clicked.connect(self.deleted_book, self.status_id)

        self.setLayout(self.layout)

    def to_left_book(self) -> None:
        """
        Перемещает книгу на одни статус левее если он существует
        """
        book = BookBox(self.book_name, self.author, self.year, self.status_id - 1, self.main_update, self.main_layout)
        self.main_layout.itemAtPosition(0, self.status_id - 1).group_box.layout.addWidget(book)
        self.main_layout.itemAtPosition(0, self.status_id - 1).group_box.books.append(book)
        self.deleted_book()

    def to_right_book(self) -> None:
        """
        Перемещает книгу на один статус правее если он существует
        """
        book = BookBox(self.book_name, self.author, self.year, self.status_id + 1, self.main_update, self.main_layout)
        self.main_layout.itemAtPosition(0, self.status_id + 1).group_box.layout.addWidget(book)
        self.main_layout.itemAtPosition(0, self.status_id + 1).group_box.books.append(book)
        self.deleted_book()

    def deleted_book(self) -> None:
        """
        Удаляет книгу из текущиего статуса
        """
        self.deleteLater()

    def edit_book(self) -> None:
        """
        Меняет текущую книгу, позволяет руками установить название, автора и год первого издания.
        Сейчас не перерисовывает после изменения виджет, только после сдига будут видны изменения.
        """
        book_name, ok_1 = QInputDialog.getText(self, ENTER_BOOK_NAME, ENTER_BOOK_NAME)
        author_name, ok_2 = QInputDialog.getText(self, ENTER_AUTHOR_NAME, ENTER_AUTHOR_NAME)
        year, ok_3 = QInputDialog.getText(self, ENTER_YEAR_OF_BOOK, ENTER_YEAR_OF_BOOK)
        try:
            int_year = int(year)
        except ValueError:
            int_year = None
        if ok_1 and ok_2 and ok_3:
            self.book_name = book_name
            self.author = author_name
            self.year = int_year
            self.main_update()


class StatusGroupBox(QGroupBox):
    def __init__(self, status_id: int, main_update: Callable, main_layout) -> None:
        """
        :param status_id: Порядовый номер колоники в котором этот виджеет
        :param main_update: Обновление главного виджета
        :param main_layout: Слои главного виджета
        """
        super().__init__(BOOK_STATUS[status_id])

        self.status_id = status_id
        self.main_layout = main_layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        self.main_update = main_update

        self.books = []

        self.add_button = QPushButton(ADD_BOOK_MESSAGE)
        self.add_button.setStyleSheet(ADD_BOOK_BUTTON_CFG)
        self.add_button.clicked.connect(self.get_book, self.status_id)
        self.layout.addWidget(self.add_button)

        self.setLayout(self.layout)

    def get_book(self) -> None:
        """
        Получает название книги, автора и год, которые пользователь ввводит.
        Если название книги уже есть в списки доступных книг, то остальные поля будут заполнены автопатичкески.
        """
        book_name, ok_1 = QInputDialog.getText(self, ENTER_BOOK_NAME, ENTER_BOOK_NAME)
        plain_titile = get_plain_titile(book_name)
        if plain_titile in all_available_books:
            self.add_book(*all_available_books[plain_titile])
        else:
            author_name, ok_2 = QInputDialog.getText(self, ENTER_AUTHOR_NAME, ENTER_AUTHOR_NAME)
            year, ok_3 = QInputDialog.getText(self, ENTER_YEAR_OF_BOOK, ENTER_YEAR_OF_BOOK)
            try:
                int_year = int(year)
            except ValueError:
                int_year = None
            if ok_1 and ok_2 and ok_3:
                self.add_book(book_name, author_name, int_year)

    def add_book(self, book_name: str, author_name: str, year: Optional[int]) -> None:
        """
        Добавляет книгу к текущему слою
        :param book_name: название книги
        :param author_name: автор произведения
        :param year: Год первого издания
        """
        book = BookBox(book_name, author_name, year, self.status_id, self.main_update, self.main_layout)
        self.books.append(book)
        self.layout.addWidget(book)


class StatusBoxLayout(QVBoxLayout):
    def __init__(self, status_id: int, main_update: Callable, main_layout) -> None:
        """
        :param status_id: Порядовый номер колоники в котором этот виджеет
        :param main_update: Обновление главного виджета
        :param main_layout: Слои главного виджета
        """
        super().__init__()
        self.status_id = status_id
        self.books = []
        self.main_update = main_update
        self.main_layout = main_layout

        self.group_box = StatusGroupBox(self.status_id, self.main_update, self.main_layout)
        self.addWidget(self.group_box)


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.width = MAIN_WINDOW_WIDTH
        self.height = MAIN_WINDOW_HEIGHT
        self.setWindowTitle(APPLICATION_TITLE)
        width_center, height_center = self.center()
        self.setGeometry(width_center, height_center, self.width, self.height)
        self.layout = QGridLayout()

        for status_id in range(STATUS_COUNTS):
            status_box = StatusBoxLayout(status_id, self.update, self.layout)
            self.layout.addLayout(status_box, 0, status_id)

        self.setLayout(self.layout)

    def center(self) -> tuple[int, int]:
        """
        Выдает координаты при которых окно будет отображаться точно по центу.
        """
        screen = QDesktopWidget().screenGeometry()
        width = (screen.width() - self.width) // 2
        height = (screen.height() - self.height) // 2
        return width, height


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
