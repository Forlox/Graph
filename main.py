import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from Grid import Grid
from GridMenu import GridMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        mainLay = QHBoxLayout()
        mainLay.setContentsMargins(5, 5, 5, 5)

        self.grid = Grid()
        self.menu = GridMenu(self.grid)
        self.menu.setFixedWidth(300)

        self.menu.stepYChanged.connect(self.grid.setYStep)
        self.menu.pointsChanged.connect(self.grid.setPoints)
        self.grid.pointsProcessed.connect(self.menu.updateLegend)
        self.menu.refreshRequested.connect(self.refresh_functions)

        # Обновляем размер окна при изменении точек
        self.grid.pointsProcessed.connect(self.adjustWindowSize)

        mainLay.addWidget(self.grid)
        mainLay.addWidget(self.menu)

        container = QWidget()
        container.setLayout(mainLay)
        self.setCentralWidget(container)
        self.adjustWindowSize()

    def refresh_functions(self):
        self.grid.functions = self.grid.getFuncs()  # Перечитываем функции из файла
        self.grid.update()  # Перерисовываем графики
        self.menu.updateLegend()  # Обновляем легенду

    def adjustWindowSize(self):
        self.resize(self.grid.sizeHint().width(), 600)
        self.setMinimumSize(self.grid.minimumSizeHint().width() + 350, 400)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())