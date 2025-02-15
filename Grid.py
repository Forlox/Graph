from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QRect

class Grid(QWidget):
    def __init__(self, countOfDiagrams, zeroLine):
        super().__init__()
        self.countOfDiagrams = countOfDiagrams
        self.zeroLine = zeroLine

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black, 5)
        painter.setPen(pen)

        ### Параметры ###
        border = 60
        stepX = self.width() // 5  # Шаг по оси X
        stepY = 60
        ##############

        # Прямоугольник
        rectWidth = self.countOfDiagrams * stepX
        rectHeight = ((self.height() - 2 * border) // stepY) * stepY

        if (rectHeight // stepY) % 2 == 1 and self.zeroLine != 1 and self.zeroLine != 2:
            rectHeight -= stepY

        painter.drawRect(border, border, rectWidth, rectHeight)

        # Сетка по оси X
        pen.setWidth(1)
        pen.setStyle(Qt.DashDotLine)
        painter.setPen(pen)

        for x in range(border + stepX, border + rectWidth, stepX):
            painter.drawLine(x, border, x, border + rectHeight)

        # Сетка по оси Y
        for y in range(border + stepY, border + rectHeight, stepY):
            painter.drawLine(border, y, border + rectWidth, y)

        # Нулевая линия
        pen.setWidth(2)
        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)
        if self.zeroLine == 1:
            painter.drawLine(border, border + rectHeight - stepY, rectWidth + border, border + rectHeight - stepY)
        elif self.zeroLine == 2:
            painter.drawLine(border, border + stepY, rectWidth + border, border + stepY)
        else:
            painter.drawLine(border, border + rectHeight // 2, rectWidth + border, border + rectHeight // 2)

        # Подписи осей
        font = painter.font()
        fontAxisSize = 12
        font.setPointSize(fontAxisSize)
        painter.setFont(font)

        painter.drawText(QRect(border, border + rectHeight + fontAxisSize*3, rectWidth, fontAxisSize*2), Qt.AlignCenter, "Ось X")

        painter.save()
        painter.translate(border - fontAxisSize * 2, border + rectHeight / 2)
        painter.rotate(-90)  # Поворачиваем текст влево
        painter.drawText(QRect(-rectHeight // 2, -fontAxisSize*3, rectHeight, fontAxisSize * 2), Qt.AlignCenter, "Ось Y")
        painter.restore()