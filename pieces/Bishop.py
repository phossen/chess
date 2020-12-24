from .Piece import Piece
from board.Color import Color


class Bishop(Piece):
    def __init__(self, color: Color, x: int, y: int, tile_size: int):
        super().__init__(color)
        if self.color == Color.WHITE:
            self.image = Piece.get_asset('assets/whiteBishop.png', tile_size)
        else:
            self.image = Piece.get_asset('assets/blackBishop.png', tile_size)
        self.rect = self.image.get_rect(topleft=(x, y))

    def get_legal_positions(self, board: dict, position: tuple) -> list:
        return []
