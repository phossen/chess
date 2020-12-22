import pygame
import os
from board.Color import Color


class Figure(pygame.sprite.Sprite):
    def __init__(self, color: Color):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.color = color

    def is_legal_move(self, board: dict, old_position: tuple, new_position: tuple) -> bool:
        # TODO: Check for legal figure move
        # Check if same position
        # Check for same color
        # Check if legal pattern
        # Check if move possible due to other figures
        return old_position!=new_position
    
    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, i):
        self.rect.x = i

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, i):
        self.rect.y = i
    
    @staticmethod
    def get_asset(path: str, tile_size: int):
        return pygame.transform.scale(pygame.image.load(os.path.normpath(path)).convert_alpha(),
                                                                         (tile_size, tile_size))
