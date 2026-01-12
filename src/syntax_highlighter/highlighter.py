from docx.shared import Pt, RGBColor
from docx.text.paragraph import Paragraph
from pygments.lexers import get_lexer_by_name
from PyQt6.QtGui import (
    QColor,
    QFont,
    QSyntaxHighlighter,
    QTextCharFormat,
    QTextCursor,
)


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

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

            fmt.setFontWeight(
                QFont.Weight.Bold if style_data["bold"] else QFont.Weight.Normal
            )

            fmt.setFontItalic(style_data["italic"])

            self.format_styles[token_type] = fmt

    def highlightBlock(self, text):
        """Подсвечивает блок текста"""
        lexer = get_lexer_by_name("python", stripall=False)
        tokens = list(lexer.get_tokens(text))[0:-1]

        cursor = QTextCursor(self.document())

        position = self.currentBlock().position()
        for token_type, value in tokens:
            length = len(value)

            cursor.setPosition(position)
            position += length
            cursor.setPosition(position, QTextCursor.MoveMode.KeepAnchor)

            fmt = self.get_format_for_token(token_type)

            if length > 0 and fmt is not None:
                cursor.mergeCharFormat(fmt)

    def get_format_for_token(self, token_type) -> QTextCharFormat | None:
        """Получает формат для типа токена"""
        while token_type:
            if token_type in self.format_styles:
                return self.format_styles[token_type]
            token_type = token_type.parent

        return None

    def get_word_format_block(
        self, paragraph: Paragraph, text: str, font: QFont
    ):
        """Получает Word-форматирование для блока текста"""
        lexer = get_lexer_by_name("python", stripall=False)
        tokens = list(lexer.get_tokens(text))[0:-1]

        for token_type, value in tokens:
            run = paragraph.add_run(value)

            fmt = self.get_format_for_token(token_type)

            run.font.name = font.family()

            run.font.size = Pt(font.pointSize())

            if fmt is not None:
                run.font.bold = fmt.fontWeight() == QFont.Weight.Bold
                run.font.italic = fmt.fontItalic()
                color = fmt.foreground().color()
                run.font.color.rgb = RGBColor(
                    color.red(), color.green(), color.blue()
                )
