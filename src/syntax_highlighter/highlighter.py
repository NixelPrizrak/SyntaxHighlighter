from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from PyQt5.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        document = self.document()
        if document is not None:
            document.setDefaultFont(QFont("Consolas", 10))

        # Массив для стилей форматирования
        self.format_styles = {}

    def set_style(self, style: dict):
        """Устанавливает стиль подсветки"""
        self.build_format_styles(style)
        self.rehighlight()

    def build_format_styles(self, style: dict):
        """Создает кэш форматов для быстрого доступа"""
        self.format_styles = {}

        # Создаем форматы для разных типов токенов
        for token_type, style_data in style.items():
            fmt = QTextCharFormat()

            # Цвет текста
            if style_data["color"]:
                color = QColor(style_data["color"])
                fmt.setForeground(color)

            # Жирный
            if style_data["bold"]:
                fmt.setFontWeight(QFont.Weight.Bold)

            # Курсив
            if style_data["italic"]:
                fmt.setFontItalic(True)

            self.format_styles[token_type] = fmt

    def highlightBlock(self, text):
        """Подсвечивает блок текста"""
        # Получаем лексер для языка
        lexer = get_lexer_by_name("python", stripall=False)

        # Лексический анализ текста
        tokens = list(lexer.get_tokens(text))

        # Применяем форматирование
        position = 0
        for token_type, value in tokens:
            length = len(value)

            # Получаем формат из кэша или создаем новый
            fmt = self.get_format_for_token(token_type)

            # Применяем формат
            if length > 0 and fmt is not None:
                self.setFormat(position, length, fmt)

            position += length

    def get_format_for_token(self, token_type):
        """Получает формат для типа токена"""
        while token_type:
            if token_type in self.format_styles:
                return self.format_styles[token_type]
            token_type = token_type.parent

        return None
