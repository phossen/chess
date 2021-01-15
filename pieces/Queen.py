from .Piece import Piece
from board.Color import Color


class Queen(Piece):
    def __init__(self, color: Color, x: int, y: int, tile_size: int):
        self.name = "Queen"
        self.value = 9
        super().__init__(color, x, y, tile_size)
    
    def get_legal_positions(self, board, position: tuple, include_own=False) -> list:
        legal_positions = []

        def check_direction(board, position: tuple, direction) -> list:
            legal_positions = []
            new_position = position
            for i in range(7):
                new_position = direction(new_position)
                if new_position is not None:
                    piece = board.piece_at_position(new_position)
                    if piece is not None:
                        if include_own:
                            legal_positions.append(new_position)
                            break
                        if piece.color != self.color:
                            legal_positions.append(new_position)
                        break
                    else:
                        legal_positions.append(new_position)
                else:
                    break
            return legal_positions

        for direction in [
                board.up,
                board.up_right,
                board.right,
                board.down_right,
                board.down,
                board.down_left,
                board.left,
                board.up_left]:
            legal_positions.extend(check_direction(board, position, direction))

        return legal_positions
