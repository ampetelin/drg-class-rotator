class ClassImageBuilderError(Exception):
    """Базовое исключение билдера изображений классов"""


class ClassImageNotFoundError(ClassImageBuilderError):
    """Изображение класса не найдено"""
