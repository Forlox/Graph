from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QPolygon
from PySide6.QtCore import Qt, QRect, Signal, QPoint, QSize
import math


class Grid(QWidget):
    pointsProcessed = Signal()

    def __init__(self):
        super().__init__()
        self.countOfDiagrams = 3
        self.functions = self.getFuncs()
        self.points = [1, 2, 3]
        self.stepY = 1
        self.border_left = 90
        self.border_right = 60
        self.padding_top = 20
        self.padding_bottom = 40
        self.point_spacing = 60
        self.perspective_depth = 10

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
        self.updateGeometry()  # Обновляем геометрию при изменении точек
        self.pointsProcessed.emit()
        self.update()

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
        if not results or not any(results):
            return 10, -10

        point_sums = []
        for point_results in results:
            positive_sum = 0
            negative_sum = 0
            for val in point_results:
                if val is not None:
                    if val > 0:
                        positive_sum += val
                    else:
                        negative_sum += val
            point_sums.append((positive_sum, negative_sum))

        max_positive = max(ps[0] for ps in point_sums) if any(ps[0] > 0 for ps in point_sums) else 0
        min_negative = min(ps[1] for ps in point_sums) if any(ps[1] < 0 for ps in point_sums) else 0

        max_val = math.ceil((max_positive + self.stepY) / self.stepY) * self.stepY
        min_val = math.floor((min_negative - self.stepY) / self.stepY) * self.stepY

        if max_val == 0 and min_val == 0:
            max_val, min_val = self.stepY, -self.stepY

        return max_val, min_val

    def sizeHint(self):
        min_width = self.border_left + self.border_right + len(self.points) * self.point_spacing
        return QSize(min_width, 400)  # Фиксированная высота 400, ширина зависит от точек

    def minimumSizeHint(self):
        return self.sizeHint()

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

        width = max(1, self.width() - self.border_left*2)
        height = max(1, self.height() - self.border_right - self.padding_top - self.padding_bottom)

        # Позиция нулевой линии
        if self.maxY <= 0:
            zero_y = self.padding_top
        elif self.minY >= 0:
            zero_y = self.padding_top + height
        else:
            zero_y = self.padding_top + height * (self.maxY / (self.maxY - self.minY))

        painter.setPen(QPen(Qt.black, 2))
        # # Периметр сетки
        # painter.drawLine(self.border_left + self.perspective_depth, self.padding_top - self.perspective_depth, self.border_left + self.perspective_depth + width, self.padding_top - self.perspective_depth)
        # painter.drawLine(self.border_left + self.perspective_depth, self.padding_top - self.perspective_depth, self.border_left + self.perspective_depth + width, self.padding_top - self.perspective_depth)
        # painter.drawLine(self.border_left + self.perspective_depth + width, self.padding_top - self.perspective_depth, self.border_left + self.perspective_depth + width, self.padding_top - self.perspective_depth + height)
        # painter.drawLine(self.border_left + self.perspective_depth + width, self.padding_top - self.perspective_depth + height, self.border_left + self.perspective_depth + width - self.perspective_depth, self.padding_top - self.perspective_depth + height + self.perspective_depth)
        # painter.drawLine(self.border_left + self.perspective_depth + width - self.perspective_depth, self.padding_top - self.perspective_depth + height + self.perspective_depth, self.border_left, self.padding_top - self.perspective_depth + height + self.perspective_depth)
        # painter.drawLine(self.border_left, self.padding_top - self.perspective_depth + height + self.perspective_depth, self.border_left, self.padding_top)
        # painter.drawLine(self.border_left, self.padding_top, self.border_left + self.perspective_depth, self.padding_top - self.perspective_depth)

        pen = QPen(Qt.black, 1)
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)

        # Рисуем горизонтальные линии сетки выше нуля
        if self.maxY > 0:
            y = zero_y
            step = 0
            while y >= self.padding_top:
                painter.drawLine(self.border_left + self.perspective_depth, y - self.perspective_depth,
                                 self.border_left + width + self.perspective_depth, y - self.perspective_depth)
                painter.drawText(self.border_left - self.perspective_depth * 5, y + 5, f"{step * self.stepY:.2f}")
                step += 1
                y = zero_y - step * (height / (self.maxY - self.minY)) * self.stepY
                painter.drawLine(self.border_left, y, self.border_left + self.perspective_depth,
                                 y - self.perspective_depth)

        # Рисуем горизонтальные линии сетки ниже нуля
        if self.minY < 0:
            y = zero_y
            step = 1
            while y <= self.padding_top + height:
                y = zero_y + step * (height / (self.maxY - self.minY)) * self.stepY
                if y > self.padding_top + height:
                    break
                painter.drawLine(self.border_left + self.perspective_depth, y - self.perspective_depth,
                                 self.border_left + width + self.perspective_depth, y - self.perspective_depth)
                painter.drawText(self.border_left - self.perspective_depth * 5, y + 5, f"{-step * self.stepY:.2f}")
                step += 1
                painter.drawLine(self.border_left, y, self.border_left + self.perspective_depth,
                                 y - self.perspective_depth)

        # Нулевая линия
        if self.maxY > 0 and self.minY < 0:
            # Ссветло-серый параллелограмм нулевой линии
            zero_poly = QPolygon([
                QPoint(self.border_left, zero_y),
                QPoint(self.border_left + self.perspective_depth, zero_y - self.perspective_depth),
                QPoint(self.border_left + width + self.perspective_depth, zero_y - self.perspective_depth),
                QPoint(self.border_left + width, zero_y)
            ])

            painter.setBrush(QBrush(QColor(220, 220, 220)))  # Светло-серый цвет
            painter.setPen(QPen(Qt.transparent))  # Прозрачная граница
            painter.drawPolygon(zero_poly)

            # Сама нулевая линия
            painter.setPen(QPen(Qt.black, 2))
            painter.drawLine(self.border_left + self.perspective_depth, zero_y - self.perspective_depth, self.border_left + width + self.perspective_depth, zero_y - self.perspective_depth)
            painter.drawLine(self.border_left, zero_y, self.border_left + self.perspective_depth, zero_y - self.perspective_depth)

    def draw_functions(self, painter):
        results = self.calculate_functions()
        if not results or not self.points:
            return

        width = max(1, self.width() - self.border_left - self.border_right)
        height = max(1, self.height() - self.border_right - self.padding_top - self.padding_bottom)

        # Позиция нулевой линии
        if self.maxY <= 0:
            zero_y = self.padding_top
        elif self.minY >= 0:
            zero_y = self.padding_top + height
        else:
            zero_y = self.padding_top + height * (self.maxY / (self.maxY - self.minY))

        px_per_unit_y = height / (self.maxY - self.minY) if (self.maxY - self.minY) != 0 else 0
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
                darker_color = color.darker(120)
                more_darker_color = color.darker(150)

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

                    # Рисуем боковую грань
                    painter.setBrush(QBrush(more_darker_color))
                    painter.setPen(QPen(more_darker_color, 1))
                    painter.drawPolygon(side_poly)

                    # Рисуем верхнюю грань
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

                    # Боковая грань
                    side_poly = QPolygon([
                        QPoint(x + 15, neg_y),
                        QPoint(x + 15 + self.perspective_depth, neg_y - self.perspective_depth),
                        QPoint(x + 15 + self.perspective_depth, neg_y + height_px - self.perspective_depth),
                        QPoint(x + 15, neg_y + height_px)
                    ])

                    # Рисуем боковую грань
                    painter.setBrush(QBrush(more_darker_color))
                    painter.setPen(QPen(more_darker_color, 1))
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