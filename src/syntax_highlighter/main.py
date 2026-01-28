import sys

from editor import CodeEditor
from PyQt6.QtCore import QLibraryInfo, QLocale, QTranslator
from PyQt6.QtGui import QAction, QColor, QFont, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QWidget,
)
from style import StyleSettings


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Syntax Highlighter")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        self.settings = StyleSettings()
        self.settings.style_changed.connect(self.update_style)
        main_layout.addWidget(self.settings)
        menu = self.menuBar()

        if menu is not None:
            menu.setStyleSheet("""
                QMenuBar {
                    border: none;
                    background-color: rgba(0, 0, 0, 0.3);
                }

                QMenuBar::item {
                    padding: 8px 15px;
                    font-weight: 400;
                    border-radius: 6px;
                }

                QMenuBar::item:selected {
                    background-color: rgba(0, 0, 0, 0.4);
                }

                QMenuBar::item:pressed {
                    background-color: rgba(0, 0, 0, 0.5);
                }
            """)
            file_menu = menu.addMenu("Файл")

            if file_menu is not None:
                # Кнопка экспорта в Word
                export_btn = QAction("Экспорт в Word", self)
                export_btn.triggered.connect(self.export_to_word)
                file_menu.addAction(export_btn)

        # Редактор
        self.editor = CodeEditor()
        self.update_style()
        main_layout.addWidget(self.editor)
        self.editor.text_changed()

    def update_style(self):
        self.editor.set_style(self.settings.get_style())

    def export_to_word(self):
        """Экспорт в Word"""

        try:
            doc = self.editor.to_docx()

            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить",
                f"code_python.docx",
                "Документ Word (*.docx)",
            )

            if file_name:
                doc.save(file_name)

        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось экспортировать: {str(e)}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Настройка оформления приложения
    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
    app.setPalette(dark_palette)

    app.setFont(QFont("Arial", 10))

    translator = QTranslator()
    if translator.load(
        QLocale(QLocale.Language.Russian),
        "qtbase_",
        "",
        QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath),
    ):
        app.installTranslator(translator)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
