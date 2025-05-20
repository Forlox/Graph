import math
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QWheelEvent, QMouseEvent

class Point3D:
    """Класс для представления точки в 3D пространстве"""
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z


class Edge:
    """Класс для представления ребра между двумя точками"""
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Letter3D:
    """Класс для представления 3D буквы из прямоугольных примитивов"""
    def __init__(self, char):
        self.char = char
        self.edges = []
        self.position = Point3D(0, 0, 0)
        self.rotation = Point3D(0, 0, 0)
        self.scale = Point3D(1, 1, 1)
        self.width = 1
        self.height = 1
        self.depth = 1
        self.default_size = (1, 1, 1)
        self.default_position = Point3D(0, 0, 0)
        self.default_rotation = Point3D(0, 0, 0)
        self.build_letter()

    def build_letter(self):
        """Строит каркас буквы из прямоугольных примитивов"""
        if self.char == 'Ч':
            self.build_ch()
        elif self.char == 'Ф':
            self.build_f()

    def build_ch(self):
        """Строит букву Ч из 3 прямоугольников"""
        # Основные параметры
        left = -self.width / 2
        right = self.width / 2
        front = -self.depth / 2
        back = self.depth / 2
        bottom = -self.height / 2
        top = self.height / 2
        middle = bottom + self.height / 2

        # Большая вертикальная правая палка
        self.add_rectangular(right - self.width / 4, right, front, back, bottom, top)

        # Горизонтальная палка в середине большой вертикальной
        self.add_rectangular(left, right, front, back, middle - self.height / 12, middle + self.height / 12)

        # Маленькая левая вертикальная палка от горизонтальной до верха
        self.add_rectangular(left, left + self.width / 4, front, back, middle - self.height / 12, top)

    def build_f(self):
        """Строит букву Ф из 5 прямоугольников"""
        left = -self.width / 2
        right = self.width / 2
        front = -self.depth / 2
        back = self.depth / 2
        bottom = -self.height / 2
        top = self.height / 2
        middle = bottom + self.height / 2

        # Верхняя горизонтальная перекладина
        self.add_rectangular(left, right, front, back, top - self.height / 6, top)

        # Средняя горизонтальная перекладина (на уровне середины)
        self.add_rectangular(left, right, front, back, middle - self.height / 12, middle + self.height / 12)

        # Центральная вертикальная стойка
        self.add_rectangular(-self.width / 8, self.width / 8, front, back, bottom, top)

        # Левый вертикальный прямоугольник (от середины до верха)
        self.add_rectangular(left, left + self.width / 4, front, back, middle + self.height / 12, top - self.height / 6)

        # Правый вертикальный прямоугольник (от середины до верха)
        self.add_rectangular(right - self.width / 4, right, front, back, middle + self.height / 12, top - self.height / 6)

    def add_rectangular(self, x1, x2, z1, z2, y1, y2):
        """Добавляет прямоугольный примитив в каркас"""
        # 8 вершин прямоугольника
        vertices = [
            Point3D(x1, y1, z1), Point3D(x2, y1, z1),
            Point3D(x2, y2, z1), Point3D(x1, y2, z1),
            Point3D(x1, y1, z2), Point3D(x2, y1, z2),
            Point3D(x2, y2, z2), Point3D(x1, y2, z2)
        ]

        # 12 ребер прямоугольника
        edges_indices = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Передняя грань
            (4, 5), (5, 6), (6, 7), (7, 4),  # Задняя грань
            (0, 4), (1, 5), (2, 6), (3, 7)  # Соединения перед-зад
        ]

        for start_idx, end_idx in edges_indices:
            self.edges.append(Edge(vertices[start_idx], vertices[end_idx]))

    def set_size(self, width, height, depth):
        """Устанавливает размеры буквы и перестраивает ее"""
        self.width = width
        self.height = height
        self.depth = depth
        self.edges = []
        self.build_letter()

    def transform_point(self, point):
        """Применяет преобразования к точке (масштаб, поворот, позиция)"""
        # Масштабирование
        x = point.x * self.scale.x
        y = point.y * self.scale.y
        z = point.z * self.scale.z

        # Вращение вокруг X
        if self.rotation.x:
            rad = math.radians(self.rotation.x)
            y, z = y * math.cos(rad) - z * math.sin(rad), y * math.sin(rad) + z * math.cos(rad)

        # Вращение вокруг Y
        if self.rotation.y:
            rad = math.radians(self.rotation.y)
            x, z = x * math.cos(rad) + z * math.sin(rad), -x * math.sin(rad) + z * math.cos(rad)

        # Вращение вокруг Z
        if self.rotation.z:
            rad = math.radians(self.rotation.z)
            x, y = x * math.cos(rad) - y * math.sin(rad), x * math.sin(rad) + y * math.cos(rad)

        # Позиция
        x += self.position.x
        y += self.position.y
        z += self.position.z

        return Point3D(x, y, z)

    def reset(self):
        """Сбрасывает параметры буквы к значениям по умолчанию"""
        self.set_size(*self.default_size)
        self.position = Point3D(*self.default_position.__dict__.values())
        self.rotation = Point3D(*self.default_rotation.__dict__.values())
        self.scale = Point3D(1, 1, 1)


class Scene3D(QWidget):
    """Виджет для отображения 3D сцены"""

    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.letters = []
        self.camera_pos = Point3D(0, 0, 500)
        self.camera_rot = Point3D(0, 0, 0)
        self.default_camera_pos = Point3D(0, 0, 500)
        self.default_camera_rot = Point3D(0, 0, 0)
        self.focal_length = 800
        self.show_axes = True
        self.last_mouse_pos = None
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)

    def add_letter(self, letter):
        """Добавляет букву в сцену"""
        self.letters.append(letter)

    def wheelEvent(self, event: QWheelEvent):
        """Обработка прокрутки колесика мыши для приближения/удаления"""
        delta = event.angleDelta().y() / 2  # Уменьшаем скорость в 2 раза
        self.camera_pos.z = max(100, min(1000, self.camera_pos.z + delta))  # Инвертируем направление
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        """Обработка нажатия кнопки мыши"""
        if event.buttons() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        """Обработка движения мыши для вращения камеры"""
        if self.last_mouse_pos and event.buttons() == Qt.LeftButton:
            delta = event.pos() - self.last_mouse_pos
            self.camera_rot.y -= delta.x() * 0.5
            self.camera_rot.x -= delta.y() * 0.5
            self.last_mouse_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Обработка отпускания кнопки мыши"""
        self.last_mouse_pos = None

    def project_point(self, point):
        """Проецирует 3D точку на 2D плоскость с учетом перспективы"""
        # Применяем вращение камеры
        x, y, z = point.x, point.y, point.z

        # Вращение камеры вокруг X
        if self.camera_rot.x:
            rad = math.radians(self.camera_rot.x)
            y, z = y * math.cos(rad) - z * math.sin(rad), y * math.sin(rad) + z * math.cos(rad)

        # Вращение камеры вокруг Y
        if self.camera_rot.y:
            rad = math.radians(self.camera_rot.y)
            x, z = x * math.cos(rad) + z * math.sin(rad), -x * math.sin(rad) + z * math.cos(rad)

        # Вращение камеры вокруг Z
        if self.camera_rot.z:
            rad = math.radians(self.camera_rot.z)
            x, y = x * math.cos(rad) - y * math.sin(rad), x * math.sin(rad) + y * math.cos(rad)

        # Смещение камеры
        x -= self.camera_pos.x
        y -= self.camera_pos.y
        z -= self.camera_pos.z

        # Перспективная проекция
        if z != 0:
            factor = self.focal_length / (self.focal_length + z)
            x = x * factor
            y = y * factor

        # Центрируем на экране
        x += self.width() / 2
        y = self.height() / 2 - y

        return QPointF(x, y)

    def paintEvent(self, event):
        """Отрисовывает сцену"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.black)  # Черный фон

        # Отрисовка осей
        if self.show_axes:
            self.draw_axes(painter)

        # Отрисовка букв
        for letter in self.letters:
            self.draw_letter(painter, letter)

    def draw_axes(self, painter):
        """Отрисовывает оси координат"""
        center = Point3D(0, 0, 0)
        x_end = Point3D(100, 0, 0)
        y_end = Point3D(0, 100, 0)
        z_end = Point3D(0, 0, 100)

        center_proj = self.project_point(center)
        x_proj = self.project_point(x_end)
        y_proj = self.project_point(y_end)
        z_proj = self.project_point(z_end)

        painter.setPen(QPen(Qt.red, 2))
        painter.drawLine(center_proj, x_proj)
        painter.drawText(x_proj, "X")

        painter.setPen(QPen(Qt.green, 2))
        painter.drawLine(center_proj, y_proj)
        painter.drawText(y_proj, "Y")

        painter.setPen(QPen(Qt.blue, 2))
        painter.drawLine(center_proj, z_proj)
        painter.drawText(z_proj, "Z")

    def draw_letter(self, painter, letter):
        """Отрисовывает букву"""
        pen = QPen(Qt.white, 2)  # Белые линии на черном фоне
        painter.setPen(pen)

        for edge in letter.edges:
            start = letter.transform_point(edge.start)
            end = letter.transform_point(edge.end)

            start_proj = self.project_point(start)
            end_proj = self.project_point(end)

            painter.drawLine(start_proj, end_proj)

    def reset_camera(self):
        """Сбрасывает параметры камеры в положение по умолчанию"""
        self.camera_pos = Point3D(*self.default_camera_pos.__dict__.values())
        self.camera_rot = Point3D(*self.default_camera_rot.__dict__.values())
        self.update()
