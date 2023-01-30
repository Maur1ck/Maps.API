import os
import sys
import requests
from io import BytesIO
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit, QLabel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 500)
        self.setWindowTitle('Maps.API')

        self.name_label = QLabel(self)
        self.name_label.setText("Запрос(3.123,3.123): ")
        self.name_label.move(10, 10)

        self.name_input = QLineEdit(self)
        self.name_input.move(120, 7)
        self.name_input.setText("Для next тз")
        self.name_input.setDisabled(True)

        self.image = QLabel(self)
        self.image.move(0, 50)
        self.image.resize(600, 450)

        self.delta = "10"
        self.getImage()

    def getImage(self):
        print(self.delta)
        map_params = {
            "ll": "37.530887,55.70311",
            "z": self.delta,
            "l": "map"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.draw_img()

    def draw_img(self):
        print(1)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if int(self.delta) < 17:
                self.delta = str(int(self.delta) + 1)
        if event.key() == Qt.Key_PageDown:
            if int(self.delta) > 0:
                self.delta = str(int(self.delta) - 1)
        self.getImage()

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())