import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from Grid import Grid
from GridMenu import GridMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        mainLay = QHBoxLayout()
        # mainLay.setContentsMargins(0, 0, 0, 0)

        self.grid = Grid(countOfDiagrams=3, zeroLine=0)
        self.menu = GridMenu(self.grid)
        self.menu.setFixedWidth(300)

        self.menu.stepYChanged.connect(self.grid.setYStep)
        self.menu.pointsChanged.connect(self.grid.setPoints)
        self.grid.pointsProcessed.connect(self.menu.updateLegend)

        mainLay.addWidget(self.grid)
        mainLay.addWidget(self.menu)

        container = QWidget()
        container.setLayout(mainLay)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setMinimumSize(800, 600)
    window.show()
    sys.exit(app.exec())