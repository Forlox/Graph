import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from a3dScene import Scene3D, Letter3D, Point3D
from a3dControlPanel import *

class MainWindow(QMainWindow):
    """Главное окно приложения"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лаба 2")
        self.setGeometry(100, 100, 1400, 800)

        # Создаем сцену
        self.scene = Scene3D()

        # Добавляем буквы
        letter_ch = Letter3D('Ч')
        letter_ch.default_size = (80, 120, 20)
        letter_ch.set_size(*letter_ch.default_size)
        letter_ch.default_position = Point3D(-100, 0, 0)
        letter_ch.position = Point3D(*letter_ch.default_position.__dict__.values())
        self.scene.add_letter(letter_ch)

        letter_f = Letter3D('Ф')
        letter_f.default_size = (100, 120, 20)
        letter_f.set_size(*letter_f.default_size)
        letter_f.default_position = Point3D(100, 0, 0)
        letter_f.position = Point3D(*letter_f.default_position.__dict__.values())
        self.scene.add_letter(letter_f)

        # Создаем панель управления
        self.control_panel = ControlPanel(self.scene)

        # Размещаем элементы
        central_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.scene)
        layout.addWidget(self.control_panel)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())