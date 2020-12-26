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
        self.value = 3

    def get_legal_positions(self, board: dict, position: tuple) -> list:
        legal_positions = []

        def check_direction(board: dict, position: tuple, direction) -> list:
            legal_positions = []
            new_position = position
            for i in range(7):
                new_position = direction(new_position)
                if new_position is not None:
                    piece = board.piece_at_position(new_position)
                    if piece is not None:
                        if piece.color != self.color:
                            legal_positions.append(new_position)
                        break
                    else:
                        legal_positions.append(new_position)
                else:
                    break
            return legal_positions

        for direction in [
                board.up_right,
                board.down_right,
                board.down_left,
                board.up_left]:
            legal_positions.extend(check_direction(board, position, direction))

        return legal_positions
