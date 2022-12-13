class RotationServiceError(Exception):
    pass


class IncorrectPlayerCountError(RotationServiceError):
    """Некорректное значение игроков"""


class UserRotationNotFoundError(RotationServiceError):
    """Ротация пользователя не найдена"""
