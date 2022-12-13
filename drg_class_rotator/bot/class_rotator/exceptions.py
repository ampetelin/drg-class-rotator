class ClassRotatorException(Exception):
    """Базовое исключение ротатора классов"""


class IncorrectCountError(ClassRotatorException):
    """Ошибка некорректного количества (игроков/дворфов)"""


class ClassUniquenessError(ClassRotatorException):
    """Ошибка уникальности классов"""


class RotationCalculationError(ClassRotatorException):
    """Ошибка расчёта ротации"""
