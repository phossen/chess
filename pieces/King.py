from .Piece import Piece
from board.Color import Color


class King(Piece):
    def __init__(self, color: Color, x: int, y: int, tile_size: int):
        self.name = "King"
        self.value = 4
        super().__init__(color, x, y, tile_size)
        self.has_moved = False

    def get_legal_positions(self, board: dict, position: tuple) -> list:
        legal_positions = []

        def positions_controlled_by_enemy(board: dict) -> set:
            legal_positions = set([])
            for y in board.y_axis:
                for x in board.x_axis:
                    current_piece = board.piece_at_position((y,x))
                    if current_piece is not None:
                        if type(current_piece) == King:
                            # TODO: Take account for King fields without causing recursion
                            continue
                        if current_piece.color != self.color:
                            legal_positions.update(current_piece.get_legal_positions(board, (y,x)))
            return legal_positions
        enemy_positions = positions_controlled_by_enemy(board)

        def check_direction(board: dict, position: tuple, direction) -> tuple:
            new_position = direction(position)
            if new_position is not None:
                piece = board.piece_at_position(new_position)
                if piece is not None:
                    if piece.color != self.color:
                        if new_position not in enemy_positions:
                            return new_position
                else:
                    if new_position not in enemy_positions:
                        return new_position
            return None

        for direction in [
                board.up,
                board.up_right,
                board.right,
                board.down_right,
                board.down,
                board.down_left,
                board.left,
                board.up_left]:
            new_pos = check_direction(board, position, direction)
            if new_pos is not None:
                legal_positions.append(new_pos)

        # TODO: Add castling
        if not self.has_moved:
            if self.color == Color.WHITE and position[0] == "1" or\
               self.color == Color.BLACK and position[0] == "8":
                    pass

        return legal_positions
