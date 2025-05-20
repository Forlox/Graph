import sys
import math
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QSlider, QDoubleSpinBox, QGroupBox, QTabWidget, QPushButton)
from PySide6.QtCore import Qt, QPointF, QPoint
from PySide6.QtGui import QPainter, QPen, QColor, QWheelEvent, QMouseEvent


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


class ControlPanel(QWidget):
    """Панель управления параметрами"""

    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.init_ui()

    def init_ui(self):
        """Инициализирует интерфейс"""
        self.setFixedWidth(400)
        main_layout = QVBoxLayout()

        # Создаем вкладки
        self.tabs = QTabWidget()

        # Вкладка для буквы Ч
        self.tab_ch = QWidget()
        self.setup_letter_tab(self.tab_ch, 'Ч')
        self.tabs.addTab(self.tab_ch, "Ч")

        # Вкладка для буквы Ф
        self.tab_f = QWidget()
        self.setup_letter_tab(self.tab_f, 'Ф')
        self.tabs.addTab(self.tab_f, "Ф")

        # Вкладка для камеры
        self.tab_camera = QWidget()
        self.setup_camera_tab(self.tab_camera)
        self.tabs.addTab(self.tab_camera, "Камера")

        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def setup_letter_tab(self, tab, letter_char):
        """Настраивает вкладку для буквы"""
        layout = QVBoxLayout()

        # Находим нужную букву в сцене
        letter = next((l for l in self.scene.letters if l.char == letter_char), None)
        if not letter:
            return

        # Кнопка сброса
        reset_btn = QPushButton("Сбросить параметры")
        reset_btn.clicked.connect(lambda: self.reset_letter(letter))
        layout.addWidget(reset_btn)

        # Размеры
        size_group = QGroupBox("Размеры")
        size_layout = QVBoxLayout()

        self.add_slider(size_layout, "Ширина:", 1, 200, letter.width,
                        lambda v: self.update_letter_size(letter, 'width', v))
        self.add_slider(size_layout, "Высота:", 1, 200, letter.height,
                        lambda v: self.update_letter_size(letter, 'height', v))
        self.add_slider(size_layout, "Глубина:", 1, 50, letter.depth,
                        lambda v: self.update_letter_size(letter, 'depth', v))

        size_group.setLayout(size_layout)
        layout.addWidget(size_group)

        # Позиция
        pos_group = QGroupBox("Позиция")
        pos_layout = QVBoxLayout()

        self.add_slider(pos_layout, "Позиция X:", -200, 200, letter.position.x,
                        lambda v: self.update_letter_pos(letter, 'x', v))
        self.add_slider(pos_layout, "Позиция Y:", -200, 200, letter.position.y,
                        lambda v: self.update_letter_pos(letter, 'y', v))
        self.add_slider(pos_layout, "Позиция Z:", -200, 200, letter.position.z,
                        lambda v: self.update_letter_pos(letter, 'z', v))

        pos_group.setLayout(pos_layout)
        layout.addWidget(pos_group)

        # Вращение
        rot_group = QGroupBox("Вращение")
        rot_layout = QVBoxLayout()

        self.add_slider(rot_layout, "Вращение X:", -180, 180, letter.rotation.x,
                        lambda v: self.update_letter_rot(letter, 'x', v))
        self.add_slider(rot_layout, "Вращение Y:", -180, 180, letter.rotation.y,
                        lambda v: self.update_letter_rot(letter, 'y', v))
        self.add_slider(rot_layout, "Вращение Z:", -180, 180, letter.rotation.z,
                        lambda v: self.update_letter_rot(letter, 'z', v))

        rot_group.setLayout(rot_layout)
        layout.addWidget(rot_group)

        tab.setLayout(layout)

    def setup_camera_tab(self, tab):
        """Настраивает вкладку для камеры"""
        layout = QVBoxLayout()

        # Кнопка сброса
        reset_btn = QPushButton("Сбросить параметры")
        reset_btn.clicked.connect(self.scene.reset_camera)
        layout.addWidget(reset_btn)

        # Подсказка для управления
        hint = QLabel("Управление камерой:\n"
                      "- ЛКМ + движение: вращение\n"
                      "- Колесико: приближение/удаление")
        layout.addWidget(hint)

        # Позиция камеры
        pos_group = QGroupBox("Позиция камеры")
        pos_layout = QVBoxLayout()

        self.add_slider(pos_layout, "Позиция X:", -500, 500, self.scene.camera_pos.x,
                        lambda v: self.update_camera_pos('x', v))
        self.add_slider(pos_layout, "Позиция Y:", -500, 500, self.scene.camera_pos.y,
                        lambda v: self.update_camera_pos('y', v))
        self.add_slider(pos_layout, "Позиция Z:", 100, 1000, self.scene.camera_pos.z,
                        lambda v: self.update_camera_pos('z', v))

        pos_group.setLayout(pos_layout)
        layout.addWidget(pos_group)

        # Вращение камеры
        rot_group = QGroupBox("Вращение камеры")
        rot_layout = QVBoxLayout()

        self.add_slider(rot_layout, "Вращение X:", -180, 180, self.scene.camera_rot.x,
                        lambda v: self.update_camera_rot('x', v))
        self.add_slider(rot_layout, "Вращение Y:", -180, 180, self.scene.camera_rot.y,
                        lambda v: self.update_camera_rot('y', v))
        self.add_slider(rot_layout, "Вращение Z:", -180, 180, self.scene.camera_rot.z,
                        lambda v: self.update_camera_rot('z', v))

        rot_group.setLayout(rot_layout)
        layout.addWidget(rot_group)

        tab.setLayout(layout)

    def add_slider(self, layout, label_text, min_val, max_val, init_val, callback):
        """Добавляет слайдер с меткой"""
        label = QLabel(label_text)
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(init_val)
        slider.valueChanged.connect(callback)

        layout.addWidget(label)
        layout.addWidget(slider)

    def update_letter_size(self, letter, dimension, value):
        """Обновляет размер буквы"""
        setattr(letter, dimension, value)
        letter.set_size(letter.width, letter.height, letter.depth)
        self.scene.update()

    def update_letter_pos(self, letter, axis, value):
        """Обновляет позицию буквы"""
        setattr(letter.position, axis, value)
        self.scene.update()

    def update_letter_rot(self, letter, axis, value):
        """Обновляет вращение буквы"""
        setattr(letter.rotation, axis, value)
        self.scene.update()

    def update_camera_pos(self, axis, value):
        """Обновляет позицию камеры"""
        setattr(self.scene.camera_pos, axis, value)
        self.scene.update()

    def update_camera_rot(self, axis, value):
        """Обновляет вращение камеры"""
        setattr(self.scene.camera_rot, axis, value)
        self.scene.update()

    def reset_letter(self, letter):
        """Сбрасывает параметры буквы"""
        letter.reset()
        self.scene.update()
        # Обновляем слайдеры
        if letter.char == 'Ч':
            tab = self.tab_ch
        elif letter.char == 'Ф':
            tab = self.tab_f

        for slider in tab.findChildren(QSlider):
            if "width" in slider.objectName():
                slider.setValue(letter.width)
            elif "height" in slider.objectName():
                slider.setValue(letter.height)
            elif "depth" in slider.objectName():
                slider.setValue(letter.depth)
            elif "pos_x" in slider.objectName():
                slider.setValue(letter.position.x)
            elif "pos_y" in slider.objectName():
                slider.setValue(letter.position.y)
            elif "pos_z" in slider.objectName():
                slider.setValue(letter.position.z)
            elif "rot_x" in slider.objectName():
                slider.setValue(letter.rotation.x)
            elif "rot_y" in slider.objectName():
                slider.setValue(letter.rotation.y)
            elif "rot_z" in slider.objectName():
                slider.setValue(letter.rotation.z)


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лаба 2")
        self.setGeometry(100, 100, 1200, 800)

        # Создаем сцену
        self.scene = Scene3D()

        # Добавляем буквы
        letter_ch = Letter3D('Ч')
        letter_ch.default_size = (80, 120, 20)
        letter_ch.set_size(*letter_ch.default_size)
        letter_ch.default_position = Point3D(-100, 0, 0)
        letter_ch.position = Point3D(*letter_ch.default_position.__dict__.values())
        self.scene.add_letter(letter_ch)

        letter_f = Letter3D('Ф')
        letter_f.default_size = (100, 120, 20)
        letter_f.set_size(*letter_f.default_size)
        letter_f.default_position = Point3D(100, 0, 0)
        letter_f.position = Point3D(*letter_f.default_position.__dict__.values())
        self.scene.add_letter(letter_f)

        # Создаем панель управления
        self.control_panel = ControlPanel(self.scene)

        # Размещаем элементы
        central_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.scene)
        layout.addWidget(self.control_panel)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())