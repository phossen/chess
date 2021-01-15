from .Piece import Piece
from board.Color import Color


class Pawn(Piece):
    def __init__(self, color: Color, x: int, y: int, tile_size: int):
        self.name = "Pawn"
        self.value = 1
        super().__init__(color, x, y, tile_size)

    def get_legal_positions(self, board, position: tuple, include_own=False) -> list:
        legal_positions = []

        # White Pawn
        if self.color == Color.WHITE:
            if int(position[0]) == 8:
                return []
            if position[0] == "2" and position[1] not in board.board["4"]:
                legal_positions.append(("4", position[1]))
            if position[1] not in board.board[chr(ord(position[0]) + 1)]:
                legal_positions.append((chr(ord(position[0]) + 1), position[1]))
            # Taking right
            if position[1] != "a":
                if chr(ord(position[1]) - 1) in board.board[chr(ord(position[0]) + 1)]:
                    if include_own:
                        legal_positions.append((chr(ord(position[0]) + 1),
                                                chr(ord(position[1]) - 1)))
                    elif board.board[chr(ord(position[0]) + 1)]\
                                    [chr(ord(position[1]) - 1)]\
                                    .color == Color.BLACK:
                        legal_positions.append((chr(ord(position[0]) + 1),
                                                chr(ord(position[1]) - 1)))
            # Taking left
            if position[1] != "h":
                if chr(ord(position[1]) + 1) in board.board[chr(ord(position[0]) + 1)]:
                    if include_own:
                        legal_positions.append((chr(ord(position[0]) + 1),
                                                chr(ord(position[1]) + 1)))
                    elif board.board[chr(ord(position[0]) + 1)]\
                                    [chr(ord(position[1]) + 1)]\
                                    .color == Color.BLACK:
                        legal_positions.append((chr(ord(position[0]) + 1),
                                                chr(ord(position[1]) + 1)))

        # Black Pawn
        else:
            if int(position[0]) == 1:
                return []
            if position[0] == "7" and position[1] not in board.board["5"]:
                legal_positions.append(("5", position[1]))
            if position[1] not in board.board[chr(ord(position[0]) - 1)]:
                legal_positions.append((chr(ord(position[0]) - 1), position[1]))
            # Taking right
            if position[1] != "a":
                if chr(ord(position[1]) - 1) in board.board[chr(ord(position[0]) - 1)]:
                    if include_own:
                        legal_positions.append((chr(ord(position[0]) - 1),
                                                chr(ord(position[1]) - 1)))
                    elif board.board[chr(ord(position[0]) - 1)]\
                                    [chr(ord(position[1]) - 1)]\
                                    .color == Color.WHITE:
                        legal_positions.append((chr(ord(position[0]) - 1),
                                                chr(ord(position[1]) - 1)))
            # Taking left
            if position[1] != "h":
                if chr(ord(position[1]) + 1) in board.board[chr(ord(position[0]) - 1)]:
                    if include_own:
                        legal_positions.append((chr(ord(position[0]) - 1),
                                                chr(ord(position[1]) + 1)))
                    elif board.board[chr(ord(position[0]) - 1)]\
                                    [chr(ord(position[1]) + 1)]\
                                    .color == Color.WHITE:
                        legal_positions.append((chr(ord(position[0]) - 1),
                                                chr(ord(position[1]) + 1)))

        return legal_positions
