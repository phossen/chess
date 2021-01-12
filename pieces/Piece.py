import pygame
import os
from board.Color import Color


class Piece(pygame.sprite.Sprite):
    def __init__(self, color: Color, x: int, y: int, tile_size: int):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.tile_size = tile_size
        self.x_axis = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.y_axis = ["8", "7", "6", "5", "4", "3", "2", "1"]
        if self.color == Color.WHITE:
            self.image = Piece.get_asset('assets/white' + self.name + '.png', tile_size)
        else:
            self.image = Piece.get_asset('assets/black' + self.name + '.png', tile_size)
        self.rect = self.image.get_rect(topleft=(x, y))

    def __name__(self):
        return self.name

    def is_legal_move(
            self,
            board: dict,
            old_position: tuple,
            new_position: tuple) -> bool:
        return new_position in self.get_legal_positions(board, old_position)

    def get_legal_positions(self, board: dict, position: tuple) -> list:
        raise NotImplementedError("Please define this function for your class.")

    def get_board_position(self):
        return (self.y_axis[int(self.y/self.tile_size)],
                self.x_axis[int(self.x/self.tile_size)])

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = value

    @staticmethod
    def get_asset(path: str, tile_size: int):
        return pygame.transform.scale(pygame.image.load(
            os.path.normpath(path)).convert_alpha(), (tile_size, tile_size))
