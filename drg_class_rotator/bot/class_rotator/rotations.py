import logging
import random
from typing import List

from bot.class_rotator.exceptions import IncorrectCountError, ClassUniquenessError, RotationCalculationError
from bot.models import DwarfClasses, Dwarf
from copy import deepcopy

logger = logging.getLogger(__name__)


def random_rotation(player_count: int, unique_classes: bool = False) -> List[Dwarf]:
    """
    Генерирует ротацию дворфов со случайными классами

    Args:
        player_count: количество игроков (1-4)
        unique_classes: признак уникальности классов между игроками

    Raises:
        IncorrectCountError: возбуждаемое исключение в случае указания количества игроков в недопустимом диапазоне

    Returns:
        Список дворфов с назначенными им классами
    """
    if not 0 < player_count < 5:
        raise IncorrectCountError('The number of players must be from 1 to 4')

    dwarves = []
    for _ in range(player_count):
        if unique_classes:
            used_classes = {dwarf.current_class for dwarf in dwarves}
            free_classes = tuple(set(DwarfClasses).difference(used_classes))
        else:
            free_classes = tuple(DwarfClasses)
        dwarves.append(Dwarf(current_class=random.choice(free_classes)))

    return dwarves


def rotation_based_on_previous_classes(dwarves: List[Dwarf]) -> List[Dwarf]:
    """
    Генерирует ротацию дворфов с учетом предыдущих классов

    Условие ротации:
        1) У каждого дворфа должен быть уникальный класс
        2) Новый класс дворфа не должен быть таким, как в двух предыдущих раундах

    Args:
        dwarves: список дворфов учавствующих в ротации (1-4)

    Raises:
        IncorrectCountError: возбуждаемое исключение в случае передачи списка дворфов, количество которого находится
            в недопустимом диапазоне
        ClassUniquenessError: возбуждаемое исключение в случае неуникальности классов дворфов
        RotationCalculationError: возбуждаемое исключение в случае невозможности расчёта ротации относительно входящего
            списка дворфов

    Returns:
        Список дворфов с новыми классами
    """
    if not 0 < len(dwarves) < 5:
        raise IncorrectCountError('The number of dwarves in the rotations must be from 1 to 4')
    if not len(dwarves) == len({dwarf.current_class for dwarf in dwarves}):
        raise ClassUniquenessError('Dwarf classes are not unique')

    _dwarves = deepcopy(dwarves)
    class_selection_attempts = {i: set() for i in range(len(_dwarves))}
    recalculation_previous_dwarf = False
    i = 0
    while i < len(_dwarves):
        logger.debug(f"Dwarf #{i + 1} {_dwarves[i]}. Previous class: {_dwarves[i].previous_class}")
        logger.debug(f"Available classes without used classes: {_dwarves[i].next_available_classes}")

        new_dwarf_classes = {_dwarves[i].current_class for i in range(i)}
        available_classes = _dwarves[i].next_available_classes - new_dwarf_classes
        logger.debug(f"Available classes without new dwarf classes: {available_classes}")

        attempts = class_selection_attempts[i]
        if recalculation_previous_dwarf:
            logger.debug(f"Incorrectly selected classes: {attempts}")
            available_classes -= attempts
            logger.debug(f"Available classes without incorrectly selected classes: {available_classes}")

        if not available_classes:
            logger.debug('Available classes is empty')
            if i == 0:
                raise RotationCalculationError('Rotation for incoming list could not be calculated')

            if attempts:
                logger.debug('Clear class selection for current dwarf')
                class_selection_attempts[i] = set()

            logger.debug('Undo previous dwarf class change')
            i -= 1
            _dwarves[i].current_class = dwarves[i].current_class
            _dwarves[i].previous_class = dwarves[i].previous_class

            recalculation_previous_dwarf = True
            continue

        new_class = random.choice(tuple(available_classes))
        logger.debug(f'New dwarf class: {new_class}')
        _dwarves[i].change_dwarf_class(new_class)
        class_selection_attempts[i] = attempts.union({new_class})

        recalculation_previous_dwarf = False

        i += 1

    return _dwarves
