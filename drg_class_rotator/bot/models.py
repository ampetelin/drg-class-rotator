from enum import Enum
from typing import Optional

from pydantic import BaseModel


class DwarfClasses(str, Enum):
    """Классы дворфов"""
    SCOUT = 'SCOUT'
    ENGINEER = 'ENGINEER'
    DRILLER = 'DRILLER'
    GUNNER = 'GUNNER'


class Dwarf(BaseModel):
    current_class: DwarfClasses
    previous_class: Optional[DwarfClasses]

    def change_dwarf_class(self, new_dwarf_class: DwarfClasses):
        """
        Изменяет класс дворфа

        Назначает значение текущего класса предыдущему классу и изменяет текущий класс на переданный `new_dwarf_class`

        Args:
            new_dwarf_class: новый класс дворфа
        """

        self.previous_class = self.current_class
        self.current_class = new_dwarf_class

    @property
    def next_available_classes(self) -> set:
        """Классы, доступные для смены в следующей ротации"""
        return set(DwarfClasses) - {self.previous_class} - {self.current_class}

    def __str__(self) -> str:
        return self.current_class.value
