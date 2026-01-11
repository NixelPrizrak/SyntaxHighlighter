from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor, QMouseEvent
from PyQt5.QtWidgets import (
    QColorDialog,
    QHBoxLayout,
    QLabel,
    QWidget,
)


class ColorPicker(QWidget):
    """Виджет выбора цвета"""

    # Сигнал об изменении цвета
    color_changed = pyqtSignal()
    current_color = "#FFFFFF"

    def __init__(self, label="", parent=None):
        super().__init__(parent)
        self.label_text = label

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)

        # Текстовая метка
        self.text_label = QLabel(self.label_text)

        # Отображение выбранного цвета
        self.color_label = QLabel()
        self.color_label.setFixedSize(60, 20)
        self.color_label.mousePressEvent = self.color_press

        layout.addWidget(self.text_label)
        layout.addWidget(self.color_label)

        self.update_color_display()

    def update_color_display(self):
        """Обновить отоброжаемый цвет"""
        self.color_label.setStyleSheet(
            f"background-color: {self.current_color};"
            "border: 1px solid #FFFFFF;"
            "border-radius: 2px;"
        )

    def color_press(self, ev: QMouseEvent | None):
        """Обработка клика по отображаемому цвету"""
        color = QColorDialog.getColor(
            QColor(self.current_color),
            self,
            f"Выберите {self.label_text.lower()}",
            QColorDialog.ShowAlphaChannel | QColorDialog.DontUseNativeDialog,
        )

        if color.isValid():
            self.set_color(color.name())

    def get_color(self):
        """Получить текущий цвет"""
        return self.current_color

    def set_color(self, color: str):
        """Установить цвет"""
        self.current_color = color
        self.update_color_display()
        self.color_changed.emit()
