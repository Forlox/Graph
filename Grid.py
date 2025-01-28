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
        rectWidth = ((self.width() - 2 * border) // step) * step
        rectHeight = ((self.height() - 2 * border) // step) * step
        if (rectHeight//step)%2==1:
            rectHeight-=step

        painter.drawRect(border, border, rectWidth, rectHeight)

        # Сетка
        pen.setWidth(1)
        pen.setStyle(Qt.DashDotLine)
        painter.setPen(pen)

        for x in range(border + step, border + rectWidth, step):
            painter.drawLine(x, border, x, border + rectHeight)

        for y in range(border + step, border + rectHeight, step):
            painter.drawLine(border, y, border + rectWidth, y)

        # Нулевая линия
        pen.setWidth(2)
        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)
        type = 0     # 1,2 - линия снизу, сверху; остальные числа, 0 - посередине
        if type==1:
            painter.drawLine(border, border+rectHeight-step, rectWidth+border, border+rectHeight-step)
        elif type==2:
            painter.drawLine(border, border+step, rectWidth+border, border+step)
        else:
            painter.drawLine(border, border+rectHeight/2, rectWidth+border, border+rectHeight/2)