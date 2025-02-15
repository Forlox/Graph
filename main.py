import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from Grid import Grid


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Параметры для сетки
        countOfDiagrams = 4
        zeroLine = 1

        # Создаем экземпляр Grid с параметрами
        self.grid = Grid(countOfDiagrams, zeroLine)
        self.setCentralWidget(self.grid)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setMinimumSize(600, 450)
    window.setWindowTitle("Graph")
    window.show()
    sys.exit(app.exec())