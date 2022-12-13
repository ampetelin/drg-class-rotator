import os
from io import BytesIO
from pathlib import Path
from typing import List

from PIL import Image, ImageDraw, ImageFont

from bot.class_image_builder.exceptions import ClassImageNotFoundError
from bot.models import DwarfClasses


class ClassImageBuilder:
    def __init__(self):
        self._image_folder = os.path.join(Path(__file__).parent, 'class_images')
        self._font_folder = os.path.join(Path(__file__).parent, 'fonts')
        self._class_image_mapper = {
            DwarfClasses.SCOUT: 'Scout.png',
            DwarfClasses.ENGINEER: 'Engineer.png',
            DwarfClasses.GUNNER: 'Gunner.png',
            DwarfClasses.DRILLER: 'Driller.png'
        }

    def get_image_of_classes(self, dwarf_classes: List[DwarfClasses]) -> bytes:
        """
        Получает объединенное изображение классов дворфов

        Args:
            dwarf_classes: список классов дворфов

        Raises:
            ClassImageNotFoundError: возбуждаемое исключение в случае отсутствия изображения класса
        """
        class_images = []
        for dwarf_class in dwarf_classes:
            class_images.append(self._get_class_image(dwarf_class))

        image = self._concatenate_class_images(class_images)
        image = self._add_numbering_and_class_names(image, dwarf_classes)

        return self._save_as_bytes(image)

    def _get_class_image(self, dwarf_class: DwarfClasses) -> Image.Image:
        """
        Получает изображение по наименованию класса дворфа

        Args:
            dwarf_class: класс дворфа

        Raises:
            ClassImageNotFoundError: возбуждаемое исключение в случае отсутствия изображения класса
        """
        try:
            return Image.open(os.path.join(self._image_folder, self._class_image_mapper[dwarf_class]))
        except FileNotFoundError:
            raise ClassImageNotFoundError(f'Image for class {dwarf_class} not found')

    @staticmethod
    def _concatenate_class_images(class_images: List[Image.Image]) -> Image.Image:
        """
        Объединяет переданные изображение в одно изображение

        Args:
            class_images: список изображений

        Returns:
            Объединенное изображение
        """
        class_image_width = class_images[0].width
        class_image_height = class_images[0].height
        image = Image.new(mode='RGBA', size=(class_image_width * len(class_images), class_image_height))

        x_offset = 0
        for class_image in class_images:
            image.paste(class_image, (x_offset, 0))
            x_offset += class_image_width

        return image

    def _add_numbering_and_class_names(self,
                                       concatenated_image: Image.Image,
                                       dwarf_classes: List[DwarfClasses]) -> Image.Image:
        """
        Добавляет нумерацию и наименования классов к изображению

        Args:
            concatenated_image: объединенное изображение классов
            dwarf_classes: список классов дворфов
        """
        text_line_height = 20

        image = Image.new(
            mode='RGBA',
            size=(concatenated_image.width, concatenated_image.height + text_line_height * 2)
        )
        image.paste(concatenated_image, (0, text_line_height))

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.join(self._font_folder, 'ArialMT.ttf'), size=24)

        class_image_width = image.width / len(dwarf_classes)
        for number, dwarf_class in enumerate(dwarf_classes):
            x = class_image_width * (number + 1) - class_image_width / 2
            draw.text(xy=(x, 0), text=str(number + 1), font=font, anchor='mt')
            draw.text(xy=(x, image.height), text=dwarf_class.value, font=font, anchor='mb')

        return image

    @staticmethod
    def _save_as_bytes(image: Image.Image, image_format: str = 'PNG') -> bytes:
        byte_array = BytesIO()
        image.save(byte_array, format=image_format)

        return byte_array.getvalue()
