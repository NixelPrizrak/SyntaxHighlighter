from color_picker import ColorPicker
from pygments.styles import get_all_styles, get_style_by_name
from pygments.token import Token
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFontDatabase, QPalette
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class StyleSettings(QScrollArea):
    """Виджет настроек стилей"""

    # Сигнал об изменении стиля
    style_changed = pyqtSignal()
    update_enabled = True

    def __init__(self):
        super().__init__()

        self.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        container = QWidget()
        self.main_layout = QVBoxLayout(container)

        self.add_header_block("Стиль")
        self.add_style_combo()
        self.add_separator()
        self.add_header_block("Шрифт")
        self.add_font_combo()
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 50)
        self.font_size.setValue(12)
        self.font_size.valueChanged.connect(self.update_style)
        self.main_layout.addWidget(self.font_size)
        self.add_separator()

        # Общие
        self.add_header_block("Общие настройки")
        self.bg_color = ColorPicker("Фон:")
        self.bg_color.color_changed.connect(self.update_style)
        self.main_layout.addWidget(
            self.bg_color, alignment=Qt.AlignmentFlag.AlignHCenter
        )

        # Блоки под разные виды токенов
        self.keywords = self.add_setting_block("Ключевые слова")
        self.classes = self.add_setting_block("Классы и модули")
        self.methods = self.add_setting_block("Функции")
        self.variables = self.add_setting_block("Переменные")
        self.constants = self.add_setting_block("Константы")
        self.strings = self.add_setting_block("Строки")
        self.literals = self.add_setting_block("Другие литералы")
        self.names = self.add_setting_block("Прочие наименования")
        self.operators = self.add_setting_block("Операторы")
        self.punctuations = self.add_setting_block("Пунктуация")
        self.comments = self.add_setting_block("Комментарии")

        self.change_style(self.style_combo.currentText())
        self.setWidget(container)

    def change_style(self, style_name: str):
        """Изменяет стиль подсветки"""
        self.update_enabled = False
        found_style = get_style_by_name(style_name)
        style = {"background": found_style.background_color, "tokens": {}}
        for token_type, style_data in found_style:
            style["tokens"][token_type] = style_data

        self.set_style(style)
        self.update_enabled = True
        self.update_style()

    def update_style(self):
        if self.update_enabled:
            self.style_changed.emit()

    def get_style(self):
        """Возвращает текущий стиль"""
        return {
            "background": self.bg_color.get_color(),
            "font": {
                "family": self.font_combo.currentText(),
                "size": self.font_size.value(),
            },
            "tokens": {
                # Комментарии
                Token.Comment: {
                    "color": self.comments["color"].get_color(),
                    "italic": self.comments["italic"].isChecked(),
                    "bold": self.comments["bold"].isChecked(),
                },
                # Ключевые слова
                Token.Keyword: {
                    "color": self.keywords["color"].get_color(),
                    "italic": self.keywords["italic"].isChecked(),
                    "bold": self.keywords["bold"].isChecked(),
                },
                # Типы
                # Token.Keyword.Type: {
                #     "color": self.comments["color"].get_color(),
                #     "italic": self.comments["italic"].isChecked(),
                #     "bold": self.comments["bold"].isChecked(),
                # },
                # Имена
                Token.Name: {
                    "color": self.names["color"].get_color(),
                    "italic": self.names["italic"].isChecked(),
                    "bold": self.names["bold"].isChecked(),
                },
                # Функции
                Token.Name.Function: {
                    "color": self.methods["color"].get_color(),
                    "italic": self.methods["italic"].isChecked(),
                    "bold": self.methods["bold"].isChecked(),
                },
                # Встроенные функции
                Token.Name.Builtin: {
                    "color": self.methods["color"].get_color(),
                    "italic": self.methods["italic"].isChecked(),
                    "bold": self.methods["bold"].isChecked(),
                },
                # Встроенные наименования
                Token.Name.Builtin.Pseudo: {
                    "color": self.variables["color"].get_color(),
                    "italic": self.variables["italic"].isChecked(),
                    "bold": self.variables["bold"].isChecked(),
                },
                # Переменные
                Token.Name.Variable: {
                    "color": self.variables["color"].get_color(),
                    "italic": self.variables["italic"].isChecked(),
                    "bold": self.variables["bold"].isChecked(),
                },
                # Переменные
                Token.Name.Constant: {
                    "color": self.constants["color"].get_color(),
                    "italic": self.constants["italic"].isChecked(),
                    "bold": self.constants["bold"].isChecked(),
                },
                # Классы
                Token.Name.Class: {
                    "color": self.classes["color"].get_color(),
                    "italic": self.classes["italic"].isChecked(),
                    "bold": self.classes["bold"].isChecked(),
                },
                # Пространства имён
                Token.Name.Namespace: {
                    "color": self.classes["color"].get_color(),
                    "italic": self.classes["italic"].isChecked(),
                    "bold": self.classes["bold"].isChecked(),
                },
                # Литералы(числа и др.)
                Token.Literal: {
                    "color": self.literals["color"].get_color(),
                    "italic": self.literals["italic"].isChecked(),
                    "bold": self.literals["bold"].isChecked(),
                },
                # Строки
                Token.Literal.String: {
                    "color": self.strings["color"].get_color(),
                    "italic": self.strings["italic"].isChecked(),
                    "bold": self.strings["bold"].isChecked(),
                },
                # Операторы
                Token.Operator: {
                    "color": self.operators["color"].get_color(),
                    "italic": self.operators["italic"].isChecked(),
                    "bold": self.operators["bold"].isChecked(),
                },
                # Пунктуация
                Token.Punctuation: {
                    "color": self.punctuations["color"].get_color(),
                    "italic": self.punctuations["italic"].isChecked(),
                    "bold": self.punctuations["bold"].isChecked(),
                },
            },
        }

    def set_style(self, style: dict):
        """Присваивает настройки стиля элементам интерфейса"""
        self.bg_color.set_color(style["background"])

        self.set_style_block(style, self.keywords, Token.Keyword)
        self.set_style_block(style, self.classes, Token.Name.Class)
        self.set_style_block(style, self.methods, Token.Name.Function)
        self.set_style_block(style, self.variables, Token.Name.Variable)
        self.set_style_block(style, self.constants, Token.Name.Constant)
        self.set_style_block(style, self.strings, Token.Literal.String)
        self.set_style_block(style, self.literals, Token.Literal)
        self.set_style_block(style, self.names, Token.Name)
        self.set_style_block(style, self.operators, Token.Operator)
        self.set_style_block(style, self.punctuations, Token.Punctuation)
        self.set_style_block(style, self.comments, Token.Comment)

    def set_style_block(self, style: dict, block: dict, token):
        """Присваивает настройки стиля элементам отдельного блока"""
        block["color"].set_color(f"#{style['tokens'][token]['color']}")
        block["italic"].setChecked(style["tokens"][token]["italic"])
        block["bold"].setChecked(style["tokens"][token]["bold"])

    def add_style_combo(self):
        """Добавляет комбобокс с доступными стилями"""
        self.style_combo = QComboBox()
        styles = set(get_all_styles())
        selected_styles = (
            "dracula",
            "one-dark",
            "monokai",
            "native",
            "nord",
            "vim",
            "coffee",
            "fruity",
            "material",
        )

        for style in selected_styles:
            if style in styles:
                self.style_combo.addItem(style)

        self.style_combo.currentTextChanged.connect(self.change_style)
        self.main_layout.addWidget(self.style_combo)

    def add_font_combo(self):
        """Добавляет комбобокс с доступными шрифтами"""
        self.font_combo = QComboBox()
        fonts = set(QFontDatabase().families())
        selected_fonts = (
            "monospace",
            "Cascadia Code",
            "Cascadia Mono",
            "Consolas",
            "Lucida Console",
            "Courier New",
            "DejaVu Sans Mono",
            "Liberation Mono",
            "Noto Mono",
            "FreeMono",
        )

        for font in selected_fonts:
            if font in fonts:
                self.font_combo.addItem(font)

        self.font_combo.currentTextChanged.connect(self.update_style)
        self.main_layout.addWidget(self.font_combo)

    def add_separator(self):
        """Добавляет разделительную линию"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)  # Вертикальная линия
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setLineWidth(1)
        separator.setPalette(QPalette(QColor("#666666")))
        self.main_layout.addWidget(separator)

    def add_setting_block(self, name: str):
        """Добавляет блок настроек"""
        self.add_separator()
        block = {}

        self.add_header_block(name)
        block["color"] = ColorPicker("Цвет:")
        block["italic"] = QCheckBox("Курсив")
        block["bold"] = QCheckBox("Жирный")
        block["color"].color_changed.connect(self.update_style)
        block["italic"].stateChanged.connect(self.update_style)
        block["bold"].stateChanged.connect(self.update_style)
        self.main_layout.addWidget(
            block["color"], alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.main_layout.addWidget(
            block["italic"], alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.main_layout.addWidget(
            block["bold"], alignment=Qt.AlignmentFlag.AlignHCenter
        )

        return block

    def add_header_block(self, name: str):
        """Добавляет заголовок блока настроек"""
        label = QLabel(name)
        font = label.font()
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(label)
