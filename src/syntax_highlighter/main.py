import sys

from editor import CodeEditor
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QWidget,
)
from style import StyleToolBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Pygments Code Editor")
        self.setGeometry(100, 100, 1200, 800)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout
        main_layout = QHBoxLayout(central_widget)

        # Панель инструментов
        self.toolbar = StyleToolBar()
        self.toolbar.style_changed.connect(self.update_style)
        main_layout.addWidget(self.toolbar)

        # Кнопка экспорта в HTML
        export_btn = QPushButton("Экспорт в HTML", self)
        export_btn.clicked.connect(self.export_to_html)
        self.toolbar.add_separator()
        self.toolbar.container_layout.addWidget(export_btn)

        # Редактор
        self.editor = CodeEditor()
        self.update_style()
        main_layout.addWidget(self.editor)

    def update_style(self):
        self.editor.set_style(self.toolbar.get_style())

    def export_to_html(self):
        """Экспорт для Word HTML с подсветкой"""
        code = self.editor.toPlainText()
        style = self.style_combo.currentText()

        try:
            lexer = get_lexer_by_name("python")
            formatter = HtmlFormatter(
                style=style, full=True, linenos=True, cssclass="highlight"
            )

            html = highlight(code, lexer, formatter)

            # Показываем диалог сохранения
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить HTML",
                f"code_python.html",
                "HTML Files (*.html *.htm)",
            )

            if file_name:
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(html)

                self.status_bar.showMessage(f"Файл сохранен: {file_name}", 3000)

        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось экспортировать: {str(e)}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Устанавливаем темную тему приложения
    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(dark_palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
