import pytest

from bot.class_rotator import exceptions
from bot.class_rotator.rotations import random_rotation, rotation_based_on_previous_classes
from bot.models import Dwarf, DwarfClasses


class TestClassRotator:
    @pytest.mark.parametrize('player_count', [1, 2, 3, 4])
    @pytest.mark.parametrize('unique_classes', [True, False])
    def test_random_rotation(self, player_count, unique_classes):
        rotation = random_rotation(player_count=player_count, unique_classes=unique_classes)

        assert len(rotation) == player_count
        assert isinstance(rotation, list)
        assert all(isinstance(x, Dwarf) for x in rotation)
        if unique_classes:
            assert len(rotation) == len(set([dwarf.current_class for dwarf in rotation]))

    def test_random_rotation_incorrect_player_count(self):
        player_count = 5
        with pytest.raises(expected_exception=exceptions.IncorrectCountError):
            random_rotation(player_count=player_count)

    def test_rotation_based_on_previous_classes_without_previous_classes(self):
        dwarves = [
            Dwarf(current_class=DwarfClasses.SCOUT),
            Dwarf(current_class=DwarfClasses.ENGINEER),
            Dwarf(current_class=DwarfClasses.DRILLER),
            Dwarf(current_class=DwarfClasses.GUNNER)
        ]
        rotation = rotation_based_on_previous_classes(dwarves)

        assert isinstance(rotation, list)
        assert all(isinstance(x, Dwarf) for x in rotation)
        assert len(rotation) == len(set([dwarf.current_class for dwarf in rotation]))
        for new_dwarf, old_dwarf in zip(rotation, dwarves):
            assert new_dwarf.current_class != old_dwarf.previous_class

    def test_rotation_based_on_previous_classes_with_previous_classes(self):
        dwarves = [
            Dwarf(current_class=DwarfClasses.SCOUT, previous_class=DwarfClasses.GUNNER),
            Dwarf(current_class=DwarfClasses.ENGINEER, previous_class=DwarfClasses.DRILLER),
            Dwarf(current_class=DwarfClasses.DRILLER, previous_class=DwarfClasses.SCOUT),
            Dwarf(current_class=DwarfClasses.GUNNER, previous_class=DwarfClasses.ENGINEER)
        ]
        rotation = rotation_based_on_previous_classes(dwarves)

        assert isinstance(rotation, list)
        assert all(isinstance(x, Dwarf) for x in rotation)
        assert len(rotation) == len(set([dwarf.current_class for dwarf in rotation]))
        for new_dwarf, old_dwarf in zip(rotation, dwarves):
            assert new_dwarf.current_class != old_dwarf.current_class
            assert new_dwarf.current_class != old_dwarf.previous_class

    def test_rotation_based_on_previous_classes_incorrect_dwarves_count(self):
        dwarves = [
            Dwarf(current_class=DwarfClasses.SCOUT),
            Dwarf(current_class=DwarfClasses.ENGINEER),
            Dwarf(current_class=DwarfClasses.DRILLER),
            Dwarf(current_class=DwarfClasses.GUNNER),
            Dwarf(current_class=DwarfClasses.GUNNER)
        ]
        with pytest.raises(exceptions.IncorrectCountError):
            rotation_based_on_previous_classes(dwarves)

    def test_rotation_based_on_previous_classes_not_unique_classes(self):
        dwarves = [Dwarf(current_class=DwarfClasses.SCOUT), Dwarf(current_class=DwarfClasses.SCOUT)]
        with pytest.raises(exceptions.ClassUniquenessError):
            rotation_based_on_previous_classes(dwarves)

    def test_rotation_based_on_previous_classes_cannot_be_calculated(self):
        dwarves = [
            Dwarf(current_class=DwarfClasses.SCOUT, previous_class=DwarfClasses.GUNNER),
            Dwarf(current_class=DwarfClasses.ENGINEER, previous_class=DwarfClasses.GUNNER),
            Dwarf(current_class=DwarfClasses.GUNNER, previous_class=DwarfClasses.DRILLER),
            Dwarf(current_class=DwarfClasses.DRILLER, previous_class=DwarfClasses.GUNNER),
        ]
        with pytest.raises(exceptions.RotationCalculationError):
            rotation_based_on_previous_classes(dwarves)
