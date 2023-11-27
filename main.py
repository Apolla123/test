import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSpinBox
import sqlite3


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = uic.loadUi('main.ui', self)

        self.setWindowTitle("Кофе")

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        layout = QVBoxLayout(self.centralWidget)

        layout.addWidget(self.ui.id_spinbox)
        layout.addWidget(self.ui.name_label)
        layout.addWidget(self.ui.roast_label)
        layout.addWidget(self.ui.grind_label)
        layout.addWidget(self.ui.taste_label)
        layout.addWidget(self.ui.price_label)
        layout.addWidget(self.ui.volume_label)

        coffee_info = self.get_coffee_info()

        self.ui.id_spinbox.setRange(1, len(coffee_info))
        self.ui.id_spinbox.valueChanged.connect(self.update_coffee_info)

        self.update_coffee_info()

    def get_coffee_info(self):
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM coffe")

        coffee_info = []
        for row in cursor.fetchall():
            info = {'ID': row[0], 'Название сорта': row[1], 'Степень обжарки': row[2], 'Молотый/в зернах': row[3],
                    'Описание вкуса': row[4], 'Цена': row[5], 'Объем упаковки': row[6]}
            coffee_info.append(info)

        cursor.close()
        connection.close()

        return coffee_info

    def update_coffee_info(self):
        selected_id = self.ui.id_spinbox.value()
        coffee_info = self.get_coffee_info()

        for info in coffee_info:
            if info['ID'] == selected_id:
                self.ui.name_label.setText(f"Название сорта: {info['Название сорта']}")
                self.ui.roast_label.setText(f"Степень обжарки: {info['Степень обжарки']}")
                self.ui.grind_label.setText(f"Молотый/в зернах: {info['Молотый/в зернах']}")
                self.ui.taste_label.setText(f"Описание вкуса: {info['Описание вкуса']}")
                self.ui.price_label.setText(f"Цена: {info['Цена']}")
                self.ui.volume_label.setText(f"Объем упаковки: {info['Объем упаковки']}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec_())
