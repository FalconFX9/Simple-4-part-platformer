from os import path
import pygame
from PIL import ImageColor
from typing import Tuple


class Platform(pygame.sprite.Sprite):

    def __init__(self, width: int, x: int, y: int, color: Tuple[int, int, int] = (255, 0, 0)):
        """
        A class for the platforms
        :param width: the width of the platform
        :param x: the horizontal position of the platform
        :param y: the vertical position of the platform
        :param color: the color of the platform
        """
        super().__init__()

        # Override the image attribute
        self.image = pygame.Surface((width, 10))
        self.image.fill(color)

        # Override the rect attribute
        self.rect = self.image.get_rect()

        # Set the position to the coordinates given as arguments
        self.rect.centerx = x
        self.rect.centery = y


class Levels:

    def __init__(self):
        """
        A class that loads all the levels.
        """
        self.levels = []

    def load_all_levels(self):
        n = 0
        while path.exists('level'+str(n)+'.dat'):
            self.levels.append(self.file_to_data('level'+str(n)+'.dat'))
            n += 1

    @staticmethod
    def file_to_data(file):
        platforms = []
        pl_tag = 'platform'
        loaded_file = open(file, 'r').read()
        lines = loaded_file.splitlines()
        while lines:
            line = lines.pop(0)
            parts = line.split()
            if pl_tag == parts[0]:
                parts.pop(0)
                platforms.append(Platform(int(parts[2]), int(parts[0]), int(parts[1]), ImageColor.getcolor(parts[3], 'RGB')))

        return platforms
