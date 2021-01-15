from .Piece import Piece
from board.Color import Color


class King(Piece):
    def __init__(self, color: Color, x: int, y: int, tile_size: int):
        self.name = "King"
        self.value = 4
        super().__init__(color, x, y, tile_size)
        self.has_moved = False

    def get_legal_positions(self, board, position: tuple, include_own=False) -> list:
        legal_positions = []

        def positions_controlled_by_enemy(board) -> set:
            legal_positions = set([])
            for y in board.y_axis:
                for x in board.x_axis:
                    current_piece = board.piece_at_position((y,x))
                    if current_piece is not None:
                        if type(current_piece) == King:
                            for direction in [board.up,
                                              board.up_right,
                                              board.right,
                                              board.down_right,
                                              board.down,
                                              board.down_left,
                                              board.left,
                                              board.up_left]:
                                new_pos = direction((y,x))
                                if new_pos is not None:
                                    legal_positions.update(new_pos)
                        elif current_piece.color != self.color:
                            legal_positions.update(current_piece.get_legal_positions(board, (y,x), include_own=True))
            return legal_positions
        enemy_positions = positions_controlled_by_enemy(board)

        def check_direction(board, position: tuple, direction) -> tuple:
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

        # Castling
        if not self.has_moved:
            # White
            if self.color == Color.WHITE and position[0] == "1":
                if ("1", "e") not in enemy_positions:
                    # Short
                    rook = board.piece_at_position(("1","h"))
                    if not rook.has_moved and\
                    not board.is_occupied(("1","f")) and\
                    not board.is_occupied(("1","g")):
                        if ("1", "f") not in enemy_positions and ("1", "g") not in enemy_positions:
                            legal_positions.append(("1","g"))
                    # Long
                    rook = board.piece_at_position(("1","a"))
                    if rook is not None:
                        if not rook.has_moved and\
                        not board.is_occupied(("1","b")) and\
                        not board.is_occupied(("1","c")) and\
                        not board.is_occupied(("1","d")):
                            if ("1", "b") not in enemy_positions and ("1", "c") not in enemy_positions and ("1", "d") not in enemy_positions:
                                legal_positions.append(("1","c"))
            # Black
            elif self.color == Color.BLACK and position[0] == "8":
                if ("8", "e") not in enemy_positions:
                    # Short
                    rook = board.piece_at_position(("8","h"))
                    if rook is not None:
                        if not rook.has_moved and\
                        not board.is_occupied(("8","f")) and\
                        not board.is_occupied(("8","g")):
                            if ("8", "f") not in enemy_positions and ("8", "g") not in enemy_positions:
                                legal_positions.append(("8","g"))
                    # Long
                    rook = board.piece_at_position(("8","a"))
                    if rook is not None:
                        if not rook.has_moved and\
                        not board.is_occupied(("8","b")) and\
                        not board.is_occupied(("8","c")) and\
                        not board.is_occupied(("8","d")):
                            if ("8", "b") not in enemy_positions and ("8", "c") not in enemy_positions and ("8", "d") not in enemy_positions:
                                legal_positions.append(("8","c"))

        return legal_positions
