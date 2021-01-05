from .Piece import Piece
from board.Color import Color


class Rook(Piece):
    def __init__(self, color: Color, x: int, y: int, tile_size: int):
        self.name = "Rook"
        self.value = 5
        super().__init__(color, x, y, tile_size)
        self.has_moved = False

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

        for direction in [board.up, board.right, board.down, board.left]:
            legal_positions.extend(check_direction(board, position, direction))

        return legal_positions
