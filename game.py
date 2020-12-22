import pygame
import numpy as np
import os
from board.Board import Board
from board.Color import Color


# Init
pygame.init()
pygame.display.set_caption('Chess')
gameIcon = pygame.image.load(os.path.normpath("assets/whiteKing.png"))
pygame.display.set_icon(gameIcon)

white, black = (255,255,255), (50,50,50)
windowSize = 400
boardLength = 8
tileSize = int(windowSize/boardLength)

gameDisplay = pygame.display.set_mode((windowSize, windowSize))
gameDisplay.fill(white)

# Draw tiles
def draw_tiles(gameDisplay):
    coutner = 0
    for i in range(0, boardLength):
        for j in range(0, boardLength):
            if coutner % 2 == 0:
                pygame.draw.rect(gameDisplay, white,
                                 [tileSize*j,tileSize*i,tileSize,tileSize])
            else:
                pygame.draw.rect(gameDisplay, black,
                                 [tileSize*j,tileSize*i,tileSize,tileSize])
            coutner += 1
        coutner -= 1

# Create Board (top left is (0,0))
board = Board.create_board(tileSize)
viable_coords = [i*tileSize for i in range(boardLength)]
x_axis = ["a", "b", "c", "d", "e", "f", "g", "h"]
y_axis = ["8", "7", "6", "5", "4", "3", "2", "1"]

# Game loop
running = True
selected = None
active_player = Color.WHITE
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

        # Click on figure
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                break_loop = False
                for row in board.values():
                    if break_loop: break
                    for current_field in row.values():
                        if current_field.rect.collidepoint(event.pos) and active_player == current_field.color:
                            selected = current_field
                            if old_x is None and old_y is None:
                                old_x = current_field.x
                                old_y = current_field.y
                            selected_offset_x = current_field.x - event.pos[0]
                            selected_offset_y = current_field.y - event.pos[1]
                            break_loop = True
                            break

        # Drop figure
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if selected is not None:
                    new_x = viable_coords[np.argmin([abs(k-(event.pos[0] + selected_offset_x)) for k in viable_coords])]
                    new_y = viable_coords[np.argmin([abs(k-(event.pos[1] + selected_offset_y)) for k in viable_coords])]
                    old_position = (y_axis[(int(old_y/tileSize))], x_axis[int(old_x/tileSize)])
                    new_position = (y_axis[(int(new_y/tileSize))], x_axis[int(new_x/tileSize)])
                    
                    # TODO: Check for check and checkmate
                    if selected.is_legal_move(board, old_position, new_position):
                        selected.x = new_x
                        selected.y = new_y
                        board[new_position[0]][new_position[1]] = selected
                        del board[old_position[0]][old_position[1]]

                        # Change Player
                        active_player = Color.BLACK if active_player == Color.WHITE else Color.WHITE
                    else:
                        selected.x = old_x
                        selected.y = old_y
                    old_x = None
                    old_y = None
                    selected = None

        # Drag figure
        elif event.type == pygame.MOUSEMOTION:
            if selected is not None:
                selected.x = event.pos[0] + selected_offset_x
                selected.y = event.pos[1] + selected_offset_y
        
        # Update canvas
        draw_tiles(gameDisplay)
        for row in board.values():
            for current_field in row.values():
                gameDisplay.blit(current_field.image, current_field.rect)
        if selected is not None:
            gameDisplay.blit(selected.image, selected.rect)

        pygame.display.update()
        clock.tick(25)

pygame.quit()
