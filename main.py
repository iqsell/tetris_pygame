from preview import Preview
from settings import *
from sys import exit

# components
from game import Game
from score import Score
from random import choice

import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (QApplication, QPushButton, QLabel, QVBoxLayout,
                             QWidget, QDialog, QLineEdit, QMessageBox)


# ----------------start window----------------------
class LoginWindow(QDialog):
    def __init__(self, reg_window=None):
        super(LoginWindow, self).__init__()

        self.reg_window = reg_window

        self.setWindowTitle("Вход")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        label = QLabel('Вход')
        self.username = QLineEdit()
        self.username.setPlaceholderText('Имя')
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText('Пароль')
        button = QPushButton('Войти')
        button.clicked.connect(self.login)

        back_button = QPushButton('Назад')
        back_button.clicked.connect(self.go_back)

        layout.addWidget(label)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def login(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('users.db')

        if not db.open():
            QMessageBox.critical(self, 'Ошибка', 'Невозможно открыть базу данных')
            return

        query = QSqlQuery()
        query.prepare("SELECT * FROM users WHERE name = :name AND password = :password")
        query.bindValue(':name', self.username.text())
        query.bindValue(':password', self.password.text())
        query.exec_()

        if query.next():
            QMessageBox.information(self, 'Успех', 'Вы успешно вошли в систему!')
            self.close()
            return True
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверное имя пользователя или пароль')

        db.close()

    def go_back(self):
        if self.reg_window is not None:
            self.reg_window.show()
            self.close()


class RegisterWindow(QDialog):
    def __init__(self, reg_window=None):
        super(RegisterWindow, self).__init__()

        self.reg_window = reg_window
        self.setWindowTitle("Регистрация")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        label = QLabel('Регистрация')
        self.username = QLineEdit()
        self.username.setPlaceholderText('Имя')
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText('Пароль')
        button = QPushButton('Создать аккаунт')
        button.clicked.connect(self.register)

        back_button = QPushButton('Назад')
        back_button.clicked.connect(self.go_back)

        layout.addWidget(label)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def register(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('users.db')

        if not db.open():
            QMessageBox.critical(self, 'Ошибка', 'Невозможно открыть базу данных')
            return

        query = QSqlQuery()
        query.exec_("CREATE TABLE IF NOT EXISTS users (name TEXT, password TEXT, registration_date TEXT)")

        query.prepare("SELECT * FROM users WHERE name = :name")
        query.bindValue(':name', self.username.text())
        query.exec_()

        if query.next():
            QMessageBox.warning(self, 'Ошибка', 'Данное имя уже используется, введите другое')
        else:
            query.prepare("INSERT INTO users (name, password, registration_date) VALUES (:name, :password, :date)")
            query.bindValue(':name', self.username.text())
            query.bindValue(':password', self.password.text())
            query.bindValue(':date', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if not query.exec_():
                QMessageBox.critical(self, 'Ошибка',
                                     'Ошибка при выполнении запроса: {}'.format(query.lastError().text()))
            else:
                QMessageBox.information(self, 'Успешная регистрация', 'Аккаунт успешно создан')

                if self.LoginWindow is not None:
                    self.LoginWindow.show()
                    self.close()

        db.close()

    def go_back(self):
        if self.reg_window is not None:
            self.reg_window.show()
            self.close()


class Reg_Window(QWidget):
    def __init__(self):
        super(Reg_Window, self).__init__()

        self.setWindowTitle("Окно регистрации")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        button1 = QPushButton('Вход')
        button1.clicked.connect(self.open_login_window)

        button2 = QPushButton('Регистрация')
        button2.clicked.connect(self.open_register_window)

        layout.addWidget(button1)
        layout.addWidget(button2)

        self.setLayout(layout)

    def open_login_window(self):
        # Создаем экземпляр LoginWindow и передаем ссылку на текущий объект (self)
        # Это позволит нам вызвать метод show() этого объекта из LoginWindow
        self.login_window = LoginWindow(reg_window=self)
        self.login_window.show()
        self.close()

    def open_register_window(self):
        # Создаем экземпляр RegisterWindow и передаем ссылку на текущий объект (self)
        # Это позволит нам вызвать метод show() этого объекта из RegisterWindow
        self.register_window = RegisterWindow(reg_window=self)
        self.register_window.show()
        self.close()


app = QApplication([])

window = Reg_Window()
window.show()
app.exec_()


# ---------------pygame---------------
class Main:
    def __init__(self):

        # general
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')

        # shapes
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        # components
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()


    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape

    def run(self):

        running = True
        self.preview.start_screen()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                    # отображение
            self.display_surface.fill(GRAY)

            # компоненты

            self.game.run()
            self.score.run()

            # обновление экрана
            pygame.display.update()
            self.clock.tick()
        pygame.quit()
        exit()


if __name__ == '__main__':
    main = Main()
    main.run()
