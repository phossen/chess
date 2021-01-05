from pieces import *
from .Color import Color


class Board(object):
    def __init__(self, tileSize):
        self.tileSize = tileSize
        self.x_axis = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.y_axis = ["8", "7", "6", "5", "4", "3", "2", "1"]
        self.board = self.create_board(tileSize)

    def create_board(self, tileSize: int):
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
                            tileSize),
                        Knight(
                            Color.BLACK,
                            1 * tileSize,
                            0,
                            tileSize),
                        Bishop(
                            Color.BLACK,
                            2 * tileSize,
                            0,
                            tileSize),
                        Queen(
                            Color.BLACK,
                            3 * tileSize,
                            0,
                            tileSize),
                        King(
                            Color.BLACK,
                            4 * tileSize,
                            0,
                            tileSize),
                        Bishop(
                            Color.BLACK,
                            5 * tileSize,
                            0,
                            tileSize),
                        Knight(
                            Color.BLACK,
                            6 * tileSize,
                            0,
                            tileSize),
                        Rook(
                            Color.BLACK,
                            7 * tileSize,
                            0,
                            tileSize)])},
            "7": {
                l: f for l,
                f in zip(
                    self.x_axis,
                    [
                        Pawn(
                            Color.BLACK,
                            i * tileSize,
                            1 * tileSize,
                            tileSize) for i in range(8)])},
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
                            i * tileSize,
                            6 * tileSize,
                            tileSize) for i in range(8)])},
            "1": {
                l: f for l,
                f in zip(
                    self.x_axis,
                    [
                        Rook(
                            Color.WHITE,
                            0,
                            7 * tileSize,
                            tileSize),
                        Knight(
                            Color.WHITE,
                            1 * tileSize,
                            7 * tileSize,
                            tileSize),
                        Bishop(
                            Color.WHITE,
                            2 * tileSize,
                            7 * tileSize,
                            tileSize),
                        Queen(
                            Color.WHITE,
                            3 * tileSize,
                            7 * tileSize,
                            tileSize),
                        King(
                            Color.WHITE,
                            4 * tileSize,
                            7 * tileSize,
                            tileSize),
                        Bishop(
                            Color.WHITE,
                            5 * tileSize,
                            7 * tileSize,
                            tileSize),
                        Knight(
                            Color.WHITE,
                            6 * tileSize,
                            7 * tileSize,
                            tileSize),
                        Rook(
                            Color.WHITE,
                            7 * tileSize,
                            7 * tileSize,
                            tileSize)])}}
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
