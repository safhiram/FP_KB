import numpy as np
import pygame
import sys
import math

ROW_COUNT = 6
COL_COUNT = 7
SQUARE = 100

# Color tuple
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

height = (ROW_COUNT+1)*SQUARE
width = (COL_COUNT)*SQUARE
size = (width, height)
RAD = int(SQUARE/2 - (ROW_COUNT-1))

board_screen = pygame.display.set_mode(size)

def create_board():
    board = np.zeros((ROW_COUNT, COL_COUNT), dtype=int)
    return board

def check_move(board, col):
    return board[ROW_COUNT-1][col] == 0

def print_board(board):
    print(np.flip(board, 0)) # Di reverse secara x axis

def get_unvisited(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def fill_board(board, row, col, piece):
    board[row][col] = piece

def check_win(board, piece):
    for c in range(COL_COUNT-3): # Horizontal
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    
    for r in range(ROW_COUNT-3): # Vertical
        for c in range(COL_COUNT):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(COL_COUNT-3): # Positive Diagonal
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3]:
                return True

    for c in range(COL_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def draw_board(board):
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            pygame.draw.rect(board_screen, BLUE, pygame.Rect(c*SQUARE, r*SQUARE+SQUARE, SQUARE, SQUARE))
            pygame.draw.circle(board_screen, BLACK, (c*SQUARE+SQUARE//2, r*SQUARE+SQUARE+SQUARE//2), RAD)
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(board_screen, RED, (c*SQUARE+SQUARE//2, height-(r*SQUARE+SQUARE//2)), RAD)
            elif board[r][c] == 2:
                pygame.draw.circle(board_screen, YELLOW, (c*SQUARE+SQUARE//2, height-(r*SQUARE+SQUARE//2)), RAD)
    pygame.display.update()

board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()
myfont = pygame.font.SysFont("monospace", 75)
draw_board(board)
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(board_screen, BLACK, (0,0, width, SQUARE))
            x_pos = event.pos[0]
            if turn == 0:
                pygame.draw.circle(board_screen, RED, (x_pos, SQUARE//2), RAD)
            else:
                pygame.draw.circle(board_screen, YELLOW, (x_pos, SQUARE//2), RAD)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(board_screen, BLACK, (0,0, width, SQUARE))
            print(event.pos)
            if turn == 0:
                x_pos = event.pos[0]
                col = int(math.floor(x_pos/SQUARE))

                if check_move(board, col):
                    row = get_unvisited(board, col)
                    fill_board(board, row, col, 1)

                    if check_win(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        board_screen.blit(label, (40, 10))
                        game_over = True
            elif turn == 1:
                x_pos = event.pos[0]
                col = int(math.floor(x_pos/SQUARE))

                if check_move(board, col):
                    row = get_unvisited(board, col)
                    fill_board(board, row, col, 2)

                    if check_win(board, 2):
                        label = myfont.render("Player 2 wins!!", 2, YELLOW)
                        board_screen.blit(label, (40, 10))
                        game_over = True
            pygame.display.update()
            print_board(board)
            draw_board(board)
            turn += 1
            turn %= 2
            if game_over:
                pygame.time.wait(2000)
