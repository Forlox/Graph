from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QPolygon
from PySide6.QtCore import Qt, QRect, Signal, QPoint
import math


class Grid(QWidget):
    pointsProcessed = Signal()

    def __init__(self, countOfDiagrams, zeroLine):
        super().__init__()
        self.countOfDiagrams = countOfDiagrams
        self.zeroLine = zeroLine
        self.functions = self.getFuncs()
        self.points = [1, 2, 3]
        self.stepY = 1
        self.border_left = 90
        self.border_right = 60
        self.padding_top = 20
        self.padding_bottom = 40
        self.point_spacing = 60
        self.perspective_depth = 10  # Глубина 3D эффекта

    @staticmethod
    def getFuncs():
        return [
            {"func": "4/(1-x)", "color": QColor(Qt.red), "name": "4/(1-x)"},
            {"func": "x**2", "color": QColor(Qt.green), "name": "x²"},
            {"func": "5*math.sin(x)", "color": QColor(Qt.blue), "name": "5*sin(x)"},
            {"func": "math.log(abs(x)+1)", "color": QColor(Qt.magenta), "name": "log(|x|+1)"}
        ]

    def setPoints(self, points_str):
        points = []
        for p in points_str.split(','):
            p = p.strip()
            if not p:
                continue
            try:
                p = p.replace('pi', str(math.pi)).replace('e', str(math.e))
                points.append(float(eval(p)))
            except:
                continue
        self.points = points if points else [1, 2, 3]
        self.pointsProcessed.emit()
        self.update()
        self.adjustSize()

    def setYStep(self, step):
        try:
            step = float(step)
            self.stepY = max(0.01, step)
            self.update()
        except:
            self.stepY = 1
            self.update()

    def calculate_functions(self):
        results = []
        for point in self.points:
            point_results = []
            for func in self.functions:
                try:
                    y = eval(func["func"], {'math': math, 'x': point})
                    point_results.append(y if y is not None and not math.isnan(y) else None)
                except:
                    point_results.append(None)
            results.append(point_results)
        return results

    def determine_bounds(self, results):
        allValues = []
        for point in results:
            positiveSum = 0
            negativeSum = 0
            for val in point:
                if val is not None:
                    if val > 0:
                        positiveSum += val
                    else:
                        negativeSum += val
            if positiveSum != 0:
                allValues.append(positiveSum)
            if negativeSum != 0:
                allValues.append(negativeSum)

        if not allValues or not results:
            return 10, -10

        max_val = max(allValues) if any(v > 0 for v in allValues) else 0
        min_val = min(allValues) if any(v < 0 for v in allValues) else 0

        if max_val > 0:
            max_val = math.ceil(max_val / self.stepY) * self.stepY
        if min_val < 0:
            min_val = math.floor(min_val / self.stepY) * self.stepY

        return max(10, max_val), min(-10, min_val)

    def sizeHint(self):
        width = self.border_left + self.border_right + len(self.points) * self.point_spacing
        return super().sizeHint() if width < 800 else width

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            self.draw_grid(painter)
            self.draw_functions(painter)
            self.drawLabels(painter)
        except Exception as e:
            print(f"Ошибка при отрисовке: {e}")

    def draw_grid(self, painter):
        results = self.calculate_functions()
        max_val, min_val = self.determine_bounds(results)
        self.maxY = max_val
        self.minY = min_val

        width = max(1, self.width() - self.border_left - self.border_right)
        height = max(1, self.height() - self.border_right - self.padding_top - self.padding_bottom)

        zero_y = self.padding_top + height * (self.maxY / (self.maxY - self.minY))

        painter.setPen(QPen(Qt.black, 2))
        painter.drawRect(self.border_left, self.padding_top, width, height)

        pen = QPen(Qt.black, 1)
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)

        y = zero_y
        step = 0
        while y >= self.padding_top:
            painter.drawLine(self.border_left, y, self.border_left + width, y)
            painter.drawText(10, y + 5, f"{step * self.stepY:.2f}")
            step += 1
            y = zero_y - step * (height / (self.maxY - self.minY)) * self.stepY

        y = zero_y
        step = 1
        while y <= self.padding_top + height:
            y = zero_y + step * (height / (self.maxY - self.minY)) * self.stepY
            if y > self.padding_top + height:
                break
            painter.drawLine(self.border_left, y, self.border_left + width, y)
            painter.drawText(10, y + 5, f"{-step * self.stepY:.2f}")
            step += 1

        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(self.border_left, zero_y, self.border_left + width, zero_y)

    def draw_functions(self, painter):
        results = self.calculate_functions()
        if not results or not self.points:
            return

        width = max(1, self.width() - self.border_left - self.border_right)
        height = max(1, self.height() - self.border_right - self.padding_top - self.padding_bottom)
        zero_y = self.padding_top + height * (self.maxY / (self.maxY - self.minY))

        px_per_unit_y = height / (self.maxY - self.minY)
        x_positions = [self.border_left + 30 + i * self.point_spacing for i in range(len(self.points))]

        for i, (point, x) in enumerate(zip(self.points, x_positions)):
            pos_y = zero_y
            neg_y = zero_y

            for j, func in enumerate(self.functions):
                if j >= len(results[i]) or results[i][j] is None:
                    continue

                value = results[i][j]
                if value is None:
                    continue

                height_px = abs(value) * px_per_unit_y
                color = func["color"]
                darker_color = color.darker(120)  # Немного темнее основной цвет
                much_darker_color = color.darker(150)  # Еще темнее для боковых граней

                if value >= 0:
                    # Основной прямоугольник
                    main_rect = QRect(x - 15, pos_y - height_px, 30, height_px)

                    # Верхняя грань (параллелограмм)
                    top_poly = QPolygon([
                        QPoint(x - 15, pos_y - height_px),
                        QPoint(x - 15 + self.perspective_depth, pos_y - height_px - self.perspective_depth),
                        QPoint(x + 15 + self.perspective_depth, pos_y - height_px - self.perspective_depth),
                        QPoint(x + 15, pos_y - height_px)
                    ])

                    # Боковая грань (параллелограмм)
                    side_poly = QPolygon([
                        QPoint(x + 15, pos_y - height_px),
                        QPoint(x + 15 + self.perspective_depth, pos_y - height_px - self.perspective_depth),
                        QPoint(x + 15 + self.perspective_depth, pos_y - self.perspective_depth),
                        QPoint(x + 15, pos_y)
                    ])

                    # Рисуем боковую грань (самая темная)
                    painter.setBrush(QBrush(much_darker_color))
                    painter.setPen(QPen(much_darker_color, 1))
                    painter.drawPolygon(side_poly)

                    # Рисуем верхнюю грань (чуть темнее)
                    painter.setBrush(QBrush(darker_color))
                    painter.setPen(QPen(darker_color, 1))
                    painter.drawPolygon(top_poly)

                    # Рисуем основной прямоугольник
                    painter.setBrush(QBrush(color))
                    painter.setPen(QPen(color, 1))
                    painter.drawRect(main_rect)

                    pos_y -= height_px
                else:
                    # Основной прямоугольник (вниз от нулевой линии)
                    main_rect = QRect(x - 15, neg_y, 30, height_px)

                    # Боковая грань (параллелограмм)
                    side_poly = QPolygon([
                        QPoint(x + 15, neg_y),
                        QPoint(x + 15 + self.perspective_depth, neg_y - self.perspective_depth),
                        QPoint(x + 15 + self.perspective_depth, neg_y + height_px - self.perspective_depth),
                        QPoint(x + 15, neg_y + height_px)
                    ])

                    # Верхняя грань (прямоугольник, а не параллелограмм)
                    top_rect = QRect(x - 15, neg_y + height_px, 30, self.perspective_depth)

                    # Рисуем боковую грань
                    painter.setBrush(QBrush(much_darker_color))
                    painter.setPen(QPen(much_darker_color, 1))
                    painter.drawPolygon(side_poly)

                    # Рисуем основной прямоугольник
                    painter.setBrush(QBrush(color))
                    painter.setPen(QPen(color, 1))
                    painter.drawRect(main_rect)

                    neg_y += height_px

    def drawLabels(self, painter):
        if not self.points:
            return

        y_pos = self.height() - self.padding_bottom // 2
        x_positions = [self.border_left + 30 + i * self.point_spacing for i in range(len(self.points))]

        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        painter.setPen(QPen(Qt.black, 1))

        for point, x in zip(self.points, x_positions):
            painter.drawText(x - 15, y_pos, f"{point:.2f}")