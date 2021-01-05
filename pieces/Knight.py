from .Piece import Piece
from board.Color import Color


class Knight(Piece):
    def __init__(self, color: Color, x: int, y: int, tile_size: int):
        self.name = "Knight"
        self.value = 3
        super().__init__(color, x, y, tile_size)

    def get_legal_positions(self, board: dict, position: tuple) -> list:
        legal_positions = []

        pos1 = board.up_right(board.up(position))
        pos2 = board.up_left(board.up(position))
        pos3 = board.up_right(board.right(position))
        pos4 = board.down_right(board.right(position))
        pos5 = board.down_left(board.down(position))
        pos6 = board.down_right(board.down(position))
        pos7 = board.up_left(board.left(position))
        pos8 = board.down_left(board.left(position))

        for pos in [pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8]:
            if pos is not None:
                piece = board.piece_at_position(pos)
                if piece is not None:
                    if piece.color != self.color:
                        legal_positions.append(pos)
                else:
                    legal_positions.append(pos)

        return legal_positions
