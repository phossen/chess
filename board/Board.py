from pieces import *
from .Color import Color


class Board(object):
    def __init__(self, tileSize):
        self.tileSize = tileSize
        self.x_axis = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.y_axis = ["8", "7", "6", "5", "4", "3", "2", "1"]
        self.board = self.create_board()

    def create_board(self):
        board = {
            "8": {
                l: f for l,
                f in zip(
                    self.x_axis,
                    [
                        Rook(
                            Color.BLACK,
                            0,
                            0,
                            self.tileSize),
                        Knight(
                            Color.BLACK,
                            1 * self.tileSize,
                            0,
                            self.tileSize),
                        Bishop(
                            Color.BLACK,
                            2 * self.tileSize,
                            0,
                            self.tileSize),
                        Queen(
                            Color.BLACK,
                            3 * self.tileSize,
                            0,
                            self.tileSize),
                        King(
                            Color.BLACK,
                            4 * self.tileSize,
                            0,
                            self.tileSize),
                        Bishop(
                            Color.BLACK,
                            5 * self.tileSize,
                            0,
                            self.tileSize),
                        Knight(
                            Color.BLACK,
                            6 * self.tileSize,
                            0,
                            self.tileSize),
                        Rook(
                            Color.BLACK,
                            7 * self.tileSize,
                            0,
                            self.tileSize)])},
            "7": {
                l: f for l,
                f in zip(
                    self.x_axis,
                    [
                        Pawn(
                            Color.BLACK,
                            i * self.tileSize,
                            1 * self.tileSize,
                            self.tileSize) for i in range(8)])},
            "6": {},
            "5": {},
            "4": {},
            "3": {},
            "2": {
                l: f for l,
                f in zip(
                    self.x_axis,
                    [
                        Pawn(
                            Color.WHITE,
                            i * self.tileSize,
                            6 * self.tileSize,
                            self.tileSize) for i in range(8)])},
            "1": {
                l: f for l,
                f in zip(
                    self.x_axis,
                    [
                        Rook(
                            Color.WHITE,
                            0,
                            7 * self.tileSize,
                            self.tileSize),
                        Knight(
                            Color.WHITE,
                            1 * self.tileSize,
                            7 * self.tileSize,
                            self.tileSize),
                        Bishop(
                            Color.WHITE,
                            2 * self.tileSize,
                            7 * self.tileSize,
                            self.tileSize),
                        Queen(
                            Color.WHITE,
                            3 * self.tileSize,
                            7 * self.tileSize,
                            self.tileSize),
                        King(
                            Color.WHITE,
                            4 * self.tileSize,
                            7 * self.tileSize,
                            self.tileSize),
                        Bishop(
                            Color.WHITE,
                            5 * self.tileSize,
                            7 * self.tileSize,
                            self.tileSize),
                        Knight(
                            Color.WHITE,
                            6 * self.tileSize,
                            7 * self.tileSize,
                            self.tileSize),
                        Rook(
                            Color.WHITE,
                            7 * self.tileSize,
                            7 * self.tileSize,
                            self.tileSize)])}}
        return board

    def positions(self):
        return [j for row in self.board.values() for j in row.values()]

    def get_in_between_positions(self, position1: tuple, position2: tuple) -> list:
        positions_in_between = []
        
        if position1[0] == position2[0]:
            # Left
            if ord(position1[1]) > ord(position2[1]):
                current_pos = position1
                while True:
                    current_pos = self.left(current_pos)
                    if current_pos != position2:
                        break
                    positions_in_between.append(current_pos)
            # Right
            else:
                current_pos = position1
                while True:
                    current_pos = self.right(current_pos)
                    if current_pos != position2:
                        break
                    positions_in_between.append(current_pos)
        elif position1[1] == position2[1]:
            # Down
            if ord(position1[1]) > ord(position2[1]):
                current_pos = position1
                while True:
                    current_pos = self.down(current_pos)
                    if current_pos != position2:
                        break
                    positions_in_between.append(current_pos)
            # Up
            else:
                current_pos = position1
                while True:
                    current_pos = self.up(current_pos)
                    if current_pos != position2:
                        break
                    positions_in_between.append(current_pos)
        else:
            # Up right
            if ord(position1[0]) < ord(position2[0]) and ord(position1[1]) < ord(position2[1]):
                current_pos = position1
                while True:
                    current_pos = self.up_right(current_pos)
                    if current_pos != position2:
                        break
                    positions_in_between.append(current_pos)
            # Down right
            if ord(position1[0]) > ord(position2[0]) and ord(position1[1]) < ord(position2[1]):
                current_pos = position1
                while True:
                    current_pos = self.down_right(current_pos)
                    if current_pos != position2:
                        break
                    positions_in_between.append(current_pos)
            # Down left
            if ord(position1[0]) > ord(position2[0]) and ord(position1[1]) > ord(position2[1]):
                current_pos = position1
                while True:
                    current_pos = self.down_left(current_pos)
                    if current_pos != position2:
                        break
                    positions_in_between.append(current_pos)
            # Up left
            else:
                current_pos = position1
                while True:
                    current_pos = self.up_left(current_pos)
                    if current_pos != position2:
                        break
                    positions_in_between.append(current_pos)

        return positions_in_between

    def is_legal_position(self, position: tuple):
        return position[0] in self.y_axis and\
               position[1] in self.x_axis

    def is_occupied(self, position: tuple) -> bool:
        return position[1] in self.board[position[0]]

    def piece_at_position(self, position: tuple):
        if self.is_occupied(position):
            return self.board[position[0]][position[1]]
        return None

    def move(self, old_position: tuple, new_position: tuple):
        if self.is_occupied(new_position):
            deleted_piece = self.board[new_position[0]][new_position[1]]
        else:
            deleted_piece = None
        self.board[new_position[0]][new_position[1]] = self.board[old_position[0]][old_position[1]]
        del self.board[old_position[0]][old_position[1]]
        return deleted_piece

    # --- Board States ---
    def check_check(self, color: Color) -> bool:
        """Check if the given color is checked"""
        king_pos = 1
        legal_positions = set([])
        for position in self.positions():
            current_pos = (self.y_axis[(int(position.y/self.tileSize))], self.x_axis[int(position.x/self.tileSize)])
            if position.color != color:
                legal_positions.update(position.get_legal_positions(self, current_pos))
            elif type(position) == King:
                king_pos = current_pos
            if king_pos in legal_positions:
                return True
        return king_pos in legal_positions

    def check_checkmate(self, color: Color) -> bool:
        """Check if the given color is checkmated (Check required)"""
        # King can't make a legal move
        for position in self.positions():
            if type(position) == King and position.color == color:
                king_pos = (self.y_axis[(int(position.y/self.tileSize))], self.x_axis[int(position.x/self.tileSize)])
                king = position
                break
        
        if len(king.get_legal_positions(self, king_pos)) != 0:
            return False
        
        # Piece giving check can't be taken
        # TODO: Account for check after taking check giving piece
        for position in self.positions():
            if position.color != color:
                check_giving_piece_pos = (self.y_axis[(int(position.y/self.tileSize))], self.x_axis[int(position.x/self.tileSize)])
                if king_pos in position.get_legal_positions(self, check_giving_piece_pos):
                    check_giving_piece = position
                    break
        
        for position in self.positions():
            if position.color == color:
                current_pos = (self.y_axis[(int(position.y/self.tileSize))], self.x_axis[int(position.x/self.tileSize)])
                if check_giving_piece in position.get_legal_positions(self, current_pos):
                    return False

        # Piece can't go in between
        positions_in_between = self.get_in_between_positions(king_pos, check_giving_piece_pos)
        for position in self.positions():
            if position.color == color:
                current_pos = (self.y_axis[(int(position.y/self.tileSize))], self.x_axis[int(position.x/self.tileSize)])
                if len(set(position.get_legal_positions(self, current_pos)).intersection(set(positions_in_between))) >= 1:
                    return False
        
        return True

    def check_draw(self, color: Color) -> bool:
        """Check if given color has legal moves"""
        for position in self.positions():
            if position.color == color:
                current_pos = (self.y_axis[(int(position.y/self.tileSize))], self.x_axis[int(position.x/self.tileSize)])
                if len(position.get_legal_positions(self, current_pos)) != 0:
                    return False
        return True

    # --- Moves ---
    def up(self, position):
        if position is None:
            return None
        if position[0] == "8":
            return None
        return (chr(ord(position[0]) + 1), position[1])

    def up_right(self, position):
        if position is None:
            return None
        if position[0] == "8" or position[1] == "h":
            return None
        return (chr(ord(position[0]) + 1), chr(ord(position[1]) + 1))

    def right_up(self, position):
        return self.up_right(position)

    def right(self, position):
        if position is None:
            return None
        if position[1] == "h":
            return None
        return (position[0], chr(ord(position[1]) + 1))

    def down_right(self, position):
        if position is None:
            return None
        if position[0] == "1" or position[1] == "h":
            return None
        return (chr(ord(position[0]) - 1), chr(ord(position[1]) + 1))

    def right_down(self, position):
        return self.down_right(position)

    def down(self, position):
        if position is None:
            return None
        if position[0] == "1":
            return None
        return (chr(ord(position[0]) - 1), position[1])

    def down_left(self, position):
        if position is None:
            return None
        if position[0] == "1" or position[1] == "a":
            return None
        return (chr(ord(position[0]) - 1), chr(ord(position[1]) - 1))

    def left_down(self, position):
        return self.down_left(position)

    def left(self, position):
        if position is None:
            return None
        if position[1] == "a":
            return None
        return (position[0], chr(ord(position[1]) - 1))

    def up_left(self, position):
        if position is None:
            return None
        if position[0] == "8" or position[1] == "a":
            return None
        return (chr(ord(position[0]) + 1), chr(ord(position[1]) - 1))

    def left_up(self, position):
        return self.up_left(position)
