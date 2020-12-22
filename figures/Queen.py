from .Figure import Figure
from board.Color import Color


class Queen(Figure):
    def __init__(self, color: Color, x: int, y: int, tile_size: int):
        super().__init__(color)
        if self.color == Color.WHITE:
            self.image = Figure.get_asset('assets/whiteQueen.png', tile_size)
        else:
            self.image = Figure.get_asset('assets/blackQueen.png', tile_size)
        self.rect = self.image.get_rect(topleft=(x, y))
