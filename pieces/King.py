from .Piece import Piece
from board.Color import Color


class King(Piece):
    def __init__(self, color: Color, x: int, y: int, tile_size: int):
        super().__init__(color)
        if self.color == Color.WHITE:
            self.image = Piece.get_asset('assets/whiteKing.png', tile_size)
        else:
            self.image = Piece.get_asset('assets/blackKing.png', tile_size)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.value = 4
        self.has_moved = False

    def __name__(self):
        return "King"

    def get_legal_positions(self, board: dict, position: tuple) -> list:
        legal_positions = []

        def check_direction(board: dict, position: tuple, direction) -> tuple:
            new_position = direction(position)
            if new_position is not None:
                piece = board.piece_at_position(new_position)
                if piece is not None:
                    if piece.color != self.color:
                        # TODO: Check of position is threatend
                        return new_position
                else:
                    # TODO: Check of position is threatend
                    return new_position

        for direction in [
                board.up,
                board.up_right,
                board.right,
                board.down_right,
                board.down,
                board.down_left,
                board.left,
                board.up_left]:
            legal_positions.append(check_direction(board, position, direction))

        # TODO: Add castling
        if not self.has_moved:
            if self.color == Color.WHITE and position[0] == "1" or\
               self.color == Color.BLACK and position[0] == "8":
                    pass

        return legal_positions
