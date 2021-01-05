import pygame
import numpy as np
import os
from board.Board import Board
from board.Color import Color
from pieces import *
import logging


# Init
logging.basicConfig(filename='game.log', level=logging.DEBUG) # TODO: Change to INFO
pygame.init()
pygame.display.set_caption('Chess')
gameIcon = pygame.image.load(os.path.normpath("assets/whiteKing.png"))
pygame.display.set_icon(gameIcon)

white, black = (255, 255, 255), (50, 50, 50)
windowSize = 400
boardLength = 8
tileSize = int(windowSize / boardLength)

gameDisplay = pygame.display.set_mode((windowSize, windowSize))
gameDisplay.fill(white)

def draw_tiles(gameDisplay):
    coutner = 0
    for i in range(0, boardLength):
        for j in range(0, boardLength):
            if coutner % 2 == 0:
                pygame.draw.rect(
                    gameDisplay, white, [
                        tileSize * j, tileSize * i, tileSize, tileSize])
            else:
                pygame.draw.rect(
                    gameDisplay, black, [
                        tileSize * j, tileSize * i, tileSize, tileSize])
            coutner += 1
        coutner -= 1

def check_check(board, color: Color) -> bool:
    """Check if the given color is checked"""
    king_pos = 1
    legal_positions = set([])
    for position in board.positions():
        current_pos = (board.y_axis[(int(position.y/tileSize))], board.x_axis[int(position.x/tileSize)])
        if position.color != color:
            legal_positions.update(position.get_legal_positions(board, current_pos))
        elif type(position) == King:
            king_pos = current_pos
        if king_pos in legal_positions:
            return True
    return king_pos in legal_positions

def check_checkmate(board, color: Color) -> bool:
    """Check if the given color is checkmated (Check required)"""

    # King can't make a legal move
    for position in board.positions():
        if type(position) == King and position.color == color:
            king_pos = (board.y_axis[(int(position.y/tileSize))], board.x_axis[int(position.x/tileSize)])
            king = position
            break
    
    if len(king.get_legal_positions(board, king_pos)) != 0:
        return False
    
    # Piece giving check can't be killed
    # TODO: Account for check after killing check giving piece
    for position in board.positions():
        if position.color != color:
            check_giving_piece_pos = (board.y_axis[(int(position.y/tileSize))], board.x_axis[int(position.x/tileSize)])
            if king_pos in position.get_legal_positions(board, check_giving_piece_pos):
                check_giving_piece = position
                break
    
    for position in board.positions():
        if position.color == color:
            current_pos = (board.y_axis[(int(position.y/tileSize))], board.x_axis[int(position.x/tileSize)])
            if check_giving_piece in position.get_legal_positions(board, current_pos):
                return False

    # Piece can't go in between
    positions_in_between = board.get_in_between_positions(king_pos, check_giving_piece_pos)
    for position in board.positions():
        if position.color == color:
            current_pos = (board.y_axis[(int(position.y/tileSize))], board.x_axis[int(position.x/tileSize)])
            if len(set(position.get_legal_positions(board, current_pos)).intersection(set(positions_in_between))) >= 1:
                return False
    
    return True

def check_draw(board, color: Color) -> bool:
    """Check if given color has legal moves"""
    for position in board.positions():
        if position.color == color:
            current_pos = (board.y_axis[(int(position.y/tileSize))], board.x_axis[int(position.x/tileSize)])
            if len(position.get_legal_positions(board, current_pos)) != 0:
                return False
    return True

# Create and draw Board (top left is (0,0))
board = Board(tileSize)
viable_coords = [i * tileSize for i in range(boardLength)]
draw_tiles(gameDisplay)
for position in board.positions():
    gameDisplay.blit(position.image, position.rect)
pygame.display.update()

# Game loop
logging.info("Starting Game")
running = True
active_player = Color.WHITE
turn = 1
selected = None
old_x = None
old_y = None
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        # Click on piece
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for position in board.positions():
                    # Select piece
                    if position.rect.collidepoint(
                            event.pos) and active_player == position.color:
                        if old_x is None and old_y is None:
                            old_x = position.x
                            old_y = position.y
                        selected = position
                        selected_offset_x = position.x - event.pos[0]
                        selected_offset_y = position.y - event.pos[1]
                        logging.debug("Clicked on {} ({}{})".format(selected.name,
                            board.y_axis[(int(old_y / tileSize))], board.x_axis[int(old_x / tileSize)]))
                        break

        # Drop piece
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if selected is not None:
                    # Calculate positions
                    new_x = viable_coords[np.argmin(
                        [abs(k - (event.pos[0] + selected_offset_x)) for k in viable_coords])]
                    new_y = viable_coords[np.argmin(
                        [abs(k - (event.pos[1] + selected_offset_y)) for k in viable_coords])]
                    old_position = (
                        board.y_axis[(int(old_y / tileSize))], board.x_axis[int(old_x / tileSize)])
                    new_position = (
                        board.y_axis[(int(new_y / tileSize))], board.x_axis[int(new_x / tileSize)])
                    
                    # Try to move to new position
                    if selected.is_legal_move(board, old_position, new_position):
                        old_piece = board.move(old_position, new_position)

                        # Check if the move causes check or doesn't remove check
                        if check_check(board, active_player):
                            logging.debug("Illegal move! King is checked.")
                            selected.x = old_x
                            selected.y = old_y
                            board.board[old_position[0]][old_position[1]] = selected
                            if old_piece is not None:
                                board.board[new_position[0]][new_position[1]] = old_piece
                        else:
                            selected.x = new_x
                            selected.y = new_y

                            # Exchange pawn
                            if type(selected) == Pawn:
                                if (active_player == Color.BLACK and new_position[0] == "1") or\
                                (active_player == Color.WHITE and new_position[0] == "8"):
                                    # TODO: Exchange pawn for arbitrary other piece
                                    board.board[new_position[0]][new_position[1]] = Queen(active_player, new_x, new_y, tileSize)
                                    logging.debug("Exchanged Pawn on {}{} to Queen.".format(new_position[0], new_position[1]))
                            elif type(selected) == King:
                                selected.has_moved = True
                            elif type(selected) == Rook:
                                selected.has_moved = True

                            # Switch player
                            active_player = Color.BLACK if active_player == Color.WHITE else Color.WHITE
                            logging.info("{} {}{}{}{} {}".format(turn, old_position[0], old_position[1],
                                                                 new_position[0], new_position[1], selected.name))
                            turn += 1

                            # Check for checkmate and draw
                            if check_check(board, active_player):
                                if check_checkmate(board, active_player):
                                    logging.debug("Checkmate")
                                    running = False
                                    break
                                logging.debug("Check")
                            elif check_draw(board, active_player):
                                    logging.debug("Draw")
                                    running = False
                                    break
                    # Go back to previous position
                    else:
                        logging.debug("Not a valid move for the piece! ({}{}{}{})".format(old_position[0], old_position[1],
                                                                                          new_position[0], new_position[1]))
                        selected.x = old_x
                        selected.y = old_y

                    # Reset selected piece
                    old_x = None
                    old_y = None
                    selected = None

                    # Update canvas
                    draw_tiles(gameDisplay)
                    for position in board.positions():
                        gameDisplay.blit(position.image, position.rect)
                    pygame.display.update()

        # Drag piece
        elif event.type == pygame.MOUSEMOTION:
            if selected is not None:
                # Update position of selected
                selected.x = event.pos[0] + selected_offset_x
                selected.y = event.pos[1] + selected_offset_y

        # Update canvas
        if selected is not None:
            draw_tiles(gameDisplay)
            for position in board.positions():
                gameDisplay.blit(position.image, position.rect)
            if selected is not None:
                gameDisplay.blit(selected.image, selected.rect)
            pygame.display.update()

        clock.tick(25)

logging.debug("Qutting Game")
pygame.quit()
