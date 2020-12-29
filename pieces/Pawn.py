from .Piece import Piece
from board.Color import Color


class Pawn(Piece):
    def __init__(self, color: Color, x: int, y: int, tile_size: int):
        super().__init__(color)
        if self.color == Color.WHITE:
            self.image = Piece.get_asset('assets/whitePawn.png', tile_size)
        else:
            self.image = Piece.get_asset('assets/blackPawn.png', tile_size)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.value = 1

    def __name__(self):
        return "Pawn"

    def get_legal_positions(self, board: dict, position: tuple) -> list:
        legal_positions = []

        # White Pawn
        if self.color == Color.WHITE:
            if int(position[0]) == 8:
                return []
            if position[0] == "2" and position[1] not in board.board["4"]:
                legal_positions.append(("4", position[1]))
            if position[1] not in board.board[chr(ord(position[0]) + 1)]:
                legal_positions.append((chr(ord(position[0]) + 1), position[1]))
            if position[1] != "a":
                if chr(ord(position[1]) - 1) in board.board[chr(ord(position[0]) + 1)]:
                    if board.board[chr(ord(position[0]) + 1)]\
                                  [chr(ord(position[1]) - 1)]\
                                  .color == Color.BLACK:
                        legal_positions.append((chr(ord(position[0]) + 1),
                                                chr(ord(position[1]) - 1)))
            if position[1] != "h":
                if chr(ord(position[1]) + 1) in board.board[chr(ord(position[0]) + 1)]:
                    if board.board[chr(ord(position[0]) + 1)]\
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
            if position[1] != "a":
                if chr(ord(position[1]) - 1) in board.board[chr(ord(position[0]) - 1)]:
                    if board.board[chr(ord(position[0]) - 1)]\
                                  [chr(ord(position[1]) - 1)]\
                                  .color == Color.WHITE:
                        legal_positions.append((chr(ord(position[0]) - 1),
                                                chr(ord(position[1]) - 1)))
            if position[1] != "h":
                if chr(ord(position[1]) + 1) in board.board[chr(ord(position[0]) - 1)]:
                    if board.board[chr(ord(position[0]) - 1)]\
                                  [chr(ord(position[1]) + 1)]\
                                  .color == Color.WHITE:
                        legal_positions.append((chr(ord(position[0]) - 1),
                                                chr(ord(position[1]) + 1)))

        return legal_positions
