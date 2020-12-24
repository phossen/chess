from pieces import *
from .Color import Color


class Board(object):
    
    @staticmethod
    def create_board(tileSize: int):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        board = {"8":{l:f for l, f in zip(letters, [Rook(Color.BLACK, 0, 0, tileSize), Knight(Color.BLACK, 1*tileSize, 0, tileSize),
                                                    Bishop(Color.BLACK, 2*tileSize, 0, tileSize), King(Color.BLACK, 3*tileSize, 0, tileSize),
                                                    Queen(Color.BLACK, 4*tileSize, 0, tileSize), Bishop(Color.BLACK, 5*tileSize, 0, tileSize),
                                                    Knight(Color.BLACK, 6*tileSize, 0, tileSize), Rook(Color.BLACK, 7*tileSize, 0, tileSize)])},
                 "7":{l:f for l, f in zip(letters, [Pawn(Color.BLACK, i*tileSize, 1*tileSize, tileSize) for i in range(8)])},
                 "6":{},
                 "5":{},
                 "4":{},
                 "3":{},
                 "2":{l:f for l, f in zip(letters, [Pawn(Color.WHITE, i*tileSize, 6*tileSize, tileSize) for i in range(8)])},
                 "1":{l:f for l, f in zip(letters, [Rook(Color.WHITE, 0, 7*tileSize, tileSize), Knight(Color.WHITE, 1*tileSize, 7*tileSize, tileSize),
                                                    Bishop(Color.WHITE, 2*tileSize, 7*tileSize, tileSize), King(Color.WHITE, 3*tileSize, 7*tileSize, tileSize),
                                                    Queen(Color.WHITE, 4*tileSize, 7*tileSize, tileSize), Bishop(Color.WHITE, 5*tileSize, 7*tileSize, tileSize),
                                                    Knight(Color.WHITE, 6*tileSize, 7*tileSize, tileSize), Rook(Color.WHITE, 7*tileSize, 7*tileSize, tileSize)])}}
        return board
