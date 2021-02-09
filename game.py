import pygame
import numpy as np
import os
from board.Board import Board
from board.Color import Color
from pieces import *
import logging


# Init
logging.basicConfig(filename='game.log', level=logging.INFO)
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
last_moved_piece = None

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
                        selected.x = new_x
                        selected.y = new_y

                        # Check if the move causes check or doesn't remove check
                        if board.check_check(active_player):
                            logging.debug("Illegal move! King is checked.")
                            selected.x = old_x
                            selected.y = old_y
                            board.board[old_position[0]][old_position[1]] = selected
                            if old_piece is not None:
                                board.board[new_position[0]][new_position[1]] = old_piece
                            else:
                                del board.board[new_position[0]][new_position[1]]
                        # En Passant
                        elif type(selected) == Pawn and new_position[1] != old_position[1] and old_piece is None and last_moved_piece is not None:
                            if last_moved_piece == board.piece_at_position((old_position[0],new_position[1])):
                                del board.board[old_position[0]][new_position[1]]
                                # Switch player
                                active_player = Color.BLACK if active_player == Color.WHITE else Color.WHITE
                                logging.info("{} {}{}{}{} {}".format(turn, old_position[0], old_position[1],
                                                                    new_position[0], new_position[1], selected.name))
                                turn += 1
                                last_moved_piece = selected
                                # Check for checkmate and draw
                                if board.check_check(active_player):
                                    if board.check_checkmate(active_player):
                                        logging.debug("Checkmate")
                                        running = False
                                        break
                                    logging.debug("Check")
                                elif board.check_draw(active_player):
                                        logging.debug("Draw")
                                        running = False
                                        break
                            # Revert move
                            else:
                                logging.debug("Illegal en passant.")
                                selected.x = old_x
                                selected.y = old_y
                                board.board[old_position[0]][old_position[1]] = selected
                                del board.board[new_position[0]][new_position[1]]
                        else:
                            if type(selected) == Pawn:
                                # Exchange pawn
                                if (active_player == Color.BLACK and new_position[0] == "1") or\
                                (active_player == Color.WHITE and new_position[0] == "8"):
                                    # TODO: Exchange pawn for arbitrary other piece
                                    board.board[new_position[0]][new_position[1]] = Queen(active_player, new_x, new_y, tileSize)
                                    logging.debug("Exchanged Pawn on {}{} to {}.".format(new_position[0], new_position[1], board.board[new_position[0]][new_position[1]].name))
                            # Castling
                            elif type(selected) == King:
                                if not selected.has_moved:
                                    if active_player == Color.WHITE:
                                        if new_position == ("1","g"):
                                            logging.debug("White short castling")
                                            board.move(("1","h"), ("1","f"))
                                            board.board["1"]["f"].x = 5*tileSize
                                        elif new_position == ("1","c"):
                                            logging.debug("White long castling")
                                            board.move(("1","a"), ("1","d"))
                                            board.board["1"]["d"].x = 3*tileSize
                                    else:
                                        if new_position == ("8","g"):
                                            logging.debug("Black short castling")
                                            board.move(("8","h"), ("8","f"))
                                            board.board["8"]["f"].x = 5*tileSize
                                        elif new_position == ("8","c"):
                                            logging.debug("Black long castling")
                                            board.move(("8","a"), ("8","d"))
                                            board.board["8"]["d"].x = 3*tileSize
                                selected.has_moved = True
                            elif type(selected) == Rook:
                                selected.has_moved = True

                            # Switch player
                            active_player = Color.BLACK if active_player == Color.WHITE else Color.WHITE
                            logging.info("{} {}{}{}{} {}".format(turn, old_position[0], old_position[1],
                                                                 new_position[0], new_position[1], selected.name))
                            turn += 1
                            last_moved_piece = selected

                            # Check for checkmate and draw
                            if board.check_check(active_player):
                                if board.check_checkmate(active_player):
                                    logging.debug("Checkmate")
                                    running = False
                                    break
                                logging.debug("Check")
                            elif board.check_draw(active_player):
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
