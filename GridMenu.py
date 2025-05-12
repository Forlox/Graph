from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QLabel)
from PySide6.QtCore import Qt, Signal
import math


class GridMenu(QWidget):
    stepYChanged = Signal(float)
    pointsChanged = Signal(str)

    def __init__(self, grid):
        super().__init__()
        self.grid = grid
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        points_label = QLabel("Точки X:")
        self.layout.addWidget(points_label)

        self.points_input = QLineEdit("1, 2, 3")
        self.points_input.textChanged.connect(self.emit_points)
        self.layout.addWidget(self.points_input)

        step_label = QLabel("Шаг сетки по Y:")
        self.layout.addWidget(step_label)

        self.step_input = QLineEdit("1")
        self.step_input.textChanged.connect(self.emit_step)
        self.layout.addWidget(self.step_input)

        legend_label = QLabel("Легенда:")
        self.layout.addWidget(legend_label)

        self.legend_text = QLabel()
        self.legend_text.setWordWrap(True)
        self.layout.addWidget(self.legend_text)

        self.setLayout(self.layout)
        self.updateLegend()

    def updateLegend(self):
        if not hasattr(self.grid, 'points') or not hasattr(self.grid, 'functions'):
            return

        results = self.grid.calculate_functions()
        legendLines = []

        for func in self.grid.functions:
            values = []
            for i, point in enumerate(self.grid.points):
                if i < len(results) and len(results[i]) > self.grid.functions.index(func):
                    val = results[i][self.grid.functions.index(func)]
                    values.append(f"{val:.2f}" if val is not None else "undef")
                else:
                    values.append("undef")

            color = func["color"]
            legendLines.append(f"<span style='color: {color.name()}'>{func['name']}: {', '.join(values)}</span>")

        self.legend_text.setText("<br>".join(legendLines))

    def emit_points(self, text):
        self.pointsChanged.emit(text)

    def emit_step(self, text):
        try:
            step = text.replace('pi', str(math.pi)).replace('e', str(math.e))
            self.stepYChanged.emit(float(eval(step)))
        except:
            if text:
                self.stepYChanged.emit(1)