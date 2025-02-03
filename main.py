import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from Grid import Grid

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(Grid())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setMinimumSize(600, 450)
    #window.setFixedSize(800, 600)
    window.setWindowTitle("Graph")
    window.show()
    sys.exit(app.exec())