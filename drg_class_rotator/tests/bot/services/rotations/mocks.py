from bot.models import Dwarf, DwarfClasses

dwarves_without_previous_class = [
    Dwarf(current_class=DwarfClasses.SCOUT),
    Dwarf(current_class=DwarfClasses.ENGINEER),
    Dwarf(current_class=DwarfClasses.DRILLER),
    Dwarf(current_class=DwarfClasses.GUNNER)
]

dwarves_with_previous_class = [
    Dwarf(current_class=DwarfClasses.SCOUT, previous_class=DwarfClasses.GUNNER),
    Dwarf(current_class=DwarfClasses.ENGINEER, previous_class=DwarfClasses.DRILLER),
    Dwarf(current_class=DwarfClasses.DRILLER, previous_class=DwarfClasses.SCOUT),
    Dwarf(current_class=DwarfClasses.GUNNER, previous_class=DwarfClasses.ENGINEER)
]
