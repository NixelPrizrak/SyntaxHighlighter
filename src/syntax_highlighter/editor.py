from highlighter import Highlighter
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPalette
from PyQt5.QtWidgets import QApplication, QTextEdit


class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()

        font = QFont("Consolas", 10)
        self.setFont(font)

        # Настраиваем табуляцию
        self.setTabStopDistance(QFontMetrics(font).horizontalAdvance(" ") * 4)

        # Подсветчик
        self.highlighter = Highlighter(self.document())

        # Загружаем пример кода
        self.load_example_code()

    def set_style(self, style: dict):
        """Устанавливает стиль подсветки синтаксиса"""
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(style["background"]))
        self.setPalette(palette)
        self.highlighter.set_style(style["tokens"])

    def load_example_code(self):
        """Загружает пример кода"""
        example_code = '''# Пример Python кода с различными конструкциями
import sys
from typing import List, Optional, Dict

class Person:
    """Класс, представляющий человека"""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self._friends: List['Person'] = []

    def greet(self) -> str:
        """Возвращает приветствие"""
        return f"Привет, меня зовут {self.name}"

    def add_friend(self, friend: 'Person') -> None:
        """Добавляет друга"""
        if friend not in self._friends:
            self._friends.append(friend)

    @property
    def friend_count(self) -> int:
        """Количество друзей"""
        return len(self._friends)

    @classmethod
    def create_child(cls, name: str) -> 'Person':
        """Создает ребенка"""
        return cls(name, 0)

def calculate_statistics(numbers: List[float]) -> Dict[str, float]:
    """Вычисляет статистические показатели"""
    if not numbers:
        return {}

    total = sum(numbers)
    average = total / len(numbers)
    maximum = max(numbers)
    minimum = min(numbers)

    return {
        'total': total,
        'average': average,
        'max': maximum,
        'min': minimum
    }

# Декоратор для логирования
def log_execution(func):
    def wrapper(*args, **kwargs):
        print(f"Выполняется {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} завершена")
        return result
    return wrapper

@log_execution
def process_data(data: List[int]) -> List[int]:
    """Обрабатывает данные"""
    return [x * 2 for x in data if x > 0]

# Использование
if __name__ == "__main__":
    person = Person("Анна", 25)
    print(person.greet())

    child = Person.create_child("Максим")
    person.add_friend(child)

    data = [1, -2, 3, 4, -5]
    processed = process_data(data)
    print(f"Обработанные данные: {processed}")

    stats = calculate_statistics([10.5, 20.3, 15.7])
    print(f"Статистика: {stats}")'''

        self.setPlainText(example_code)
