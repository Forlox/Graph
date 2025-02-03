from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QRect

class Grid(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black, 5)
        painter.setPen(pen)

        ### Параметры ###
        border = 60
        step = 60
        ##############

        # Прямоугольник
        rectWidth = ((self.width() - 2 * border) // step) * step
        rectHeight = ((self.height() - 2 * border) // step) * step

        zeroLine = 1  # 1,2 - нулевая линия снизу, сверху; остальные числа, 0 - посередине

        if (rectHeight // step) % 2 == 1 and zeroLine==0:
            rectHeight -= step

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
        if zeroLine == 1:
            painter.drawLine(border, border + rectHeight - step, rectWidth + border, border + rectHeight - step)
        elif zeroLine == 2:
            painter.drawLine(border, border + step, rectWidth + border, border + step)
        else:
            painter.drawLine(border, border + rectHeight / 2, rectWidth + border, border + rectHeight / 2)

        # Подписи осей
        font = painter.font()
        fontAxisSize = 12
        font.setPointSize(fontAxisSize)
        painter.setFont(font)

        painter.drawText(QRect(border, border + rectHeight, rectWidth, fontAxisSize*2), Qt.AlignCenter, "Ось X")

        painter.save()
        painter.translate(border - fontAxisSize * 2, border + rectHeight / 2)
        painter.rotate(-90)  # Поворачиваем текст влево
        painter.drawText(QRect(-rectHeight // 2, -fontAxisSize, rectHeight, fontAxisSize * 2), Qt.AlignCenter, "Ось Y")
        painter.restore()
