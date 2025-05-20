from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QGroupBox, QTabWidget, QPushButton
from PySide6.QtCore import Qt

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


        # Позиция камеры
        pos_group = QGroupBox("Позиция камеры")
        pos_layout = QVBoxLayout()

        self.add_slider(pos_layout, "Позиция X:", -500, 500, self.scene.camera_pos.x,
                        lambda v: self.update_camera_pos('x', v))
        self.add_slider(pos_layout, "Позиция Y:", -500, 500, self.scene.camera_pos.y,
                        lambda v: self.update_camera_pos('y', v))
        self.add_slider(pos_layout, "Позиция Z:", -500, 500, self.scene.camera_pos.z,
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