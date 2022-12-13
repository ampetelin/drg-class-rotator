from bot.models import DwarfClasses
from bot.class_image_builder.builder import ClassImageBuilder


class TestClassImageBuilder:
    def setup_class(self):
        self.builder = ClassImageBuilder()

    def test_class_image_mapping(self):
        mapper_classes = sorted(self.builder._class_image_mapper.keys())
        model_classes = sorted(DwarfClasses)
        assert mapper_classes == model_classes, \
            'The class and image mapper does not contain all dwarves classes. Please add an image and complete the ' \
            'mapper. '

    def test_get_image_of_classes(self):
        dwarf_classes = [DwarfClasses.SCOUT, DwarfClasses.ENGINEER]
        image = self.builder.get_image_of_classes(dwarf_classes)

        assert isinstance(image, bytes)
