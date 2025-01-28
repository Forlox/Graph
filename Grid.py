from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt

class Grid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black, 5)
        #pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)

        ###Параметры###
        border = 30
        step = 60
        ##############

        # Прямоугольник
        width = ((self.width() - 2 * border) // step) * step
        height = ((self.height() - 2 * border) // step) * step

        painter.drawRect(border, border, width, height)

        # Сетка
        pen.setWidth(1)
        pen.setStyle(Qt.DotLine)
        painter.setPen(pen)

        for x in range(border + step, border + width, step):
            painter.drawLine(x, border, x, border + height)

        for y in range(border + step, border + height, step):
            painter.drawLine(border, y, border + width, y)
