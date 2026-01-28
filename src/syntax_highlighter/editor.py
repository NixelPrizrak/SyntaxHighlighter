from docx import Document
from docx.document import Document as DocumentObject
from docx.enum.text import WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from docx.text.paragraph import Paragraph
from pygments.lexers.python import PythonLexer
from pygments.token import Token
from PyQt6.QtGui import (
    QColor,
    QFont,
    QPalette,
    QTextCharFormat,
    QTextCursor,
)
from PyQt6.QtWidgets import QTextEdit


class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAcceptRichText(False)
        self.textChanged.connect(self.text_changed)
        # Массив для стилей форматирования
        self.format_styles = {}

        # Загрузка примера кода
        self.changed = True
        self.load_example_code()
        self.changed = False

    def text_changed(self):
        """Обновляет подсветку синтаксиса при изменении текста"""
        if self.changed:
            return
        self.changed = True
        lexer = PythonLexer()
        tokens = list(lexer.get_tokens_unprocessed(self.toPlainText()))

        cursor = QTextCursor(self.document())

        position = 0
        for i in range(len(tokens)):
            if (
                tokens[i][1] == Token.Name
                and len(tokens) > i + 1
                and tokens[i + 1][2] == "("
            ):
                token_type = Token.Name.Function
            else:
                token_type = tokens[i][1]

            value = tokens[i][2]

            length = len(value)

            cursor.setPosition(position)
            position += length
            cursor.setPosition(position, QTextCursor.MoveMode.KeepAnchor)

            fmt = self.get_format_for_token(token_type)

            if length > 0 and fmt is not None:
                cursor.mergeCharFormat(fmt)

        self.changed = False

    def set_style(self, style: dict):
        """Устанавливает стиль подсветки синтаксиса"""
        palette = self.palette()
        if palette.color(QPalette.ColorRole.Base).name() != style["background"]:
            palette.setColor(
                QPalette.ColorRole.Base, QColor(style["background"])
            )

        if (
            self.fontFamily() != style["font"]["family"]
            or self.fontPointSize() != style["font"]["size"]
        ):
            current_text = self.toPlainText()
            self.clear()
            self.setFontFamily(style["font"]["family"])
            self.setFontPointSize(style["font"]["size"])
            self.setPlainText(current_text)

        self.setPalette(palette)
        self.build_format_styles(style["tokens"])
        self.text_changed()

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

    def get_format_for_token(self, token_type) -> QTextCharFormat | None:
        """Получает формат для типа токена"""
        while token_type:
            if token_type in self.format_styles:
                return self.format_styles[token_type]
            token_type = token_type.parent

        return None

    def createMimeDataFromSelection(self):
        mime_data = super().createMimeDataFromSelection()

        if mime_data is not None:
            html = mime_data.html()

            # Добавление цвета фона для текста
            palette = self.palette()
            background = palette.color(QPalette.ColorRole.Base).name()
            i = html.find("</head>")
            html = (
                html[:i]
                + "<style>p {background-color: "
                + background
                + ";}</style>"
                + html[i:]
            )
            html = html.replace("white-space: pre-wrap", "white-space: pre", 1)

            # Добавление дополнительного абзаца в конце для правильного отображения формата последней строки
            i = html.rfind("<!--EndFragment--></p>")
            html = html[:i] + "</p><p>" + html[i:]

            mime_data.setHtml(html)

        return mime_data

    def insertFromMimeData(self, source):
        """Перехватываем вставку из буфера обмена"""
        if source is None or not source.hasFormat("text/plain"):
            return

        text = source.text()
        cursor = self.textCursor()
        cursor.insertText(text)

    def to_docx(self) -> DocumentObject:
        """Конвертирует текст в Word документ"""
        lines = self.toPlainText().splitlines()
        bg_color = self.palette().color(QPalette.ColorRole.Base)
        font = QFont(self.fontFamily(), int(self.fontPointSize()))

        doc = Document()
        section = doc.sections[0]
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

        position = 0
        for line in lines:
            paragraph = doc.add_paragraph("")
            paragraph.paragraph_format.line_spacing = 1.0
            paragraph.paragraph_format.line_spacing_rule = (
                WD_LINE_SPACING.SINGLE
            )
            paragraph.paragraph_format.space_after = Pt(0)
            paragraph.paragraph_format.space_before = Pt(0)

            self.set_paragraph_background(
                paragraph,
                RGBColor(bg_color.red(), bg_color.green(), bg_color.blue()),
            )

            self.get_word_format_block(paragraph, line, position, font)
            position += len(line) + 1

        return doc

    def set_paragraph_background(self, paragraph: Paragraph, color: RGBColor):
        """Устанавливает фон для параграфа"""
        # Получаем XML элемент параграфа
        p = paragraph._p

        # Получаем или создаем элемент форматирования параграфа
        pPr = p.get_or_add_pPr()

        # Создаем элемент заливки (shading)
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), color.__str__())  # HEX цвет без #

        # Добавляем элемент заливки к форматированию параграфа
        pPr.append(shd)

    def get_word_format_block(
        self, paragraph: Paragraph, text: str, position: int, font: QFont
    ):
        """Получает Word-форматирование для блока текста"""
        cursor = QTextCursor(self.document())

        for i in range(len(text)):
            run = paragraph.add_run(text[i])

            cursor.setPosition(position)
            cursor.movePosition(
                QTextCursor.MoveOperation.Right,
                QTextCursor.MoveMode.KeepAnchor,
                1,
            )
            position += 1
            fmt = cursor.charFormat()

            run.font.name = font.family()

            run.font.size = Pt(font.pointSize())

            if fmt is not None:
                run.font.bold = fmt.fontWeight() == QFont.Weight.Bold
                run.font.italic = fmt.fontItalic()
                color = fmt.foreground().color()
                run.font.color.rgb = RGBColor(
                    color.red(), color.green(), color.blue()
                )

    def load_example_code(self):
        """Загружает пример кода"""
        example_code = '''class SimpleCalculator:
    """Простой калькулятор"""

    def __init__(self):
        self.value = 0
        self.operations = []

    def calculate(self, operation: str, x: float, y: float = None) -> float:
        """Выполнить вычисление"""

        # Условный оператор с разными ветками
        if operation == "add":
            result = x + y
        elif operation == "multiply":
            result = x * y
        elif operation == "power":
            result = x ** y
        elif operation == "sqrt":
            # Условное выражение для обработки отрицательных чисел
            result = math.sqrt(x) if x >= 0 else -1
        else:
            result = x  # Возвращаем значение по умолчанию

        # Добавление элемента в список
        self.operations.append(f"{operation}: {x},{y if y else ''} = {result}")

        # Тернарный оператор для установки значения
        self.value = result if result > 0 else 0

        return result

    def show_history(self):
        """Показать историю операций"""
        for i, op in enumerate(self.operations, 1):
            print(f"{i}. {op}")


if __name__ == "__main__":
    import math

    calc = SimpleCalculator()

    print("Вычисления:")
    print(f"Сложение: {calc.calculate('add', 5, 3)}")
    print(f"Умножение: {calc.calculate('multiply', 4, 2)}")
    print(f"Возведение в степень: {calc.calculate('power', 2, 3)}")
    print(f"Квадратный корень: {calc.calculate('sqrt', 9)}")

    print("История операций:")
    calc.show_history()'''

        self.setPlainText(example_code)
