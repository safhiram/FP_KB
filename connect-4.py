import numpy as np
import pygame
import sys
import math
import random

ROW_COUNT = 6
COL_COUNT = 7
SQUARE = 100

# Color tuple
BLUE = (0, 0, 200)
GOLD = (255, 213, 0)
BLACK = (0, 0, 0)
GREEN = (68, 204, 0)

PLAYER_1 = 1  # player
PLAYER_2 = 2  # AI
WINDOW_SIZE = 4

height = (ROW_COUNT+1)*SQUARE
width = (COL_COUNT)*SQUARE
size = (width, height)
RAD = SQUARE//2 - (ROW_COUNT-1)
pygame.init()
board_screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("Arial", 75)


def create_board():
    board = np.zeros((ROW_COUNT, COL_COUNT), dtype=int)
    return board


def check_move(board, col):
    return board[ROW_COUNT-1][col].any() == 0


def next_move(board):
    loc = []
    for c in range(COL_COUNT):
        if check_move(board, c):
            loc.append(c)
    return loc


def print_board(board):
    print(np.flip(board, 0))  # Di reverse secara x axis


def get_unvisited(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def fill_board(board, row, col, piece):
    board[row][col] = piece


def check_win(board, piece):
    for c in range(COL_COUNT-3):  # Horizontal
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for r in range(ROW_COUNT-3):  # Vertical
        for c in range(COL_COUNT):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(COL_COUNT-3):  # Positive Diagonal
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    for c in range(COL_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def evaluate_neighbour(window, piece):
    score = 0
    if piece == PLAYER_1:
        opponent = PLAYER_2
    elif piece == PLAYER_2:
        opponent = PLAYER_1

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2
    # elif window.count(piece) == 1 and window.count(0) == 3:
    #     score += 5

    if window.count(opponent) == 3 and window.count(0) == 1:
        score -= 4

    return score


def draw_board(board):
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            pygame.draw.rect(board_screen, BLUE, pygame.Rect(
                c*SQUARE, r*SQUARE+SQUARE, SQUARE, SQUARE))
            pygame.draw.circle(
                board_screen, BLACK, (c*SQUARE+SQUARE//2, r*SQUARE+SQUARE+SQUARE//2), RAD)
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(
                    board_screen, GREEN, (c*SQUARE+SQUARE//2, height-(r*SQUARE+SQUARE//2)), RAD)
            elif board[r][c] == 2:
                pygame.draw.circle(
                    board_screen, GOLD, (c*SQUARE+SQUARE//2, height-(r*SQUARE+SQUARE//2)), RAD)
    pygame.display.update()

def is_terminal(board):
    return check_win(board, PLAYER_1) or check_win(board, PLAYER_2) or len(next_move(board)) == 0

def check_score(board, piece):
    score = 0

    # Horizontal check
    for r in range(ROW_COUNT):
        r_array = [i for i in list(board[r, :])]
        for c in range(COL_COUNT-3):
            window = r_array[c:c+WINDOW_SIZE]
            score += evaluate_neighbour(window, piece)
    # Vertical check
    for c in range(COL_COUNT):
        c_array = [i for i in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = c_array[r:r+WINDOW_SIZE]
            score += evaluate_neighbour(window, piece)
    # Diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            window = []
            for i in range(WINDOW_SIZE):
                window.append(board[r+i][c+i])
            score += evaluate_neighbour(window, piece)
    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            window = []
            for i in range(WINDOW_SIZE):
                window.append(board[r+3-i][c+i])
            score += evaluate_neighbour(window, piece)

    return score


def alpha_beta(board, state, alpha, beta, depth):
    move = next_move(board)
    terminal = is_terminal(board)

    if depth == 0 or terminal:
        if terminal:
            if check_win(board, PLAYER_1):
                return (None, -math.inf)
            elif check_win(board, PLAYER_2):
                return (None, math.inf)
            else:
                return (None, 0)
        else:
            return (None, check_score(board, PLAYER_2))

    if state:
        current_val = -math.inf
        col = random.choice(move)
        for c in move:
            r = get_unvisited(board, c)
            board_c = board.copy()
            fill_board(board_c, r, c, PLAYER_2)
            new_score = alpha_beta(board_c, False, alpha, beta, depth-1)[1]
            if new_score > current_val:
                current_val = new_score
                col = c
            alpha = max(alpha, current_val)
            if alpha >= beta:
                break

        return col, current_val
    else:
        current_val = math.inf
        col = random.choice(move)
        for c in move:
            r = get_unvisited(board, c)
            board_c = board.copy()
            fill_board(board_c, r, c, PLAYER_1)
            new_score = alpha_beta(board_c, True, alpha, beta, depth-1)[1]
            if new_score < current_val:
                current_val = new_score
                col = c
            beta = min(beta, current_val)
            if alpha >= beta:
                break
        return col, current_val

board = create_board()
print_board(board)
game_over = False
turn = 0

draw_board(board)
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(board_screen, BLACK, (0, 0, width, SQUARE))
            x_pos = event.pos[0]
            if turn == 0:
                pygame.draw.circle(board_screen, GREEN,
                                   (x_pos, SQUARE//2), RAD)
            # print("POS " + str(event.pos))
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(board_screen, BLACK, (0, 0, width, SQUARE))
            print(event.pos)
            if turn == 0:
                x_pos = event.pos[0]
                col = int(math.floor(x_pos/SQUARE))

                if check_move(board, col):
                    row = get_unvisited(board, col)
                    fill_board(board, row, col, 1)

                    if check_win(board, 1):
                        label = myfont.render("Player 1 Menang.", 1, GREEN)
                        board_screen.blit(label, (100, 10))
                        game_over = True

                    pygame.display.update()
                    print_board(board)
                    draw_board(board)
                    turn ^= 1

    # AI harus diluar event
    if turn == 1:
        col, score = alpha_beta(board, True, -math.inf, math.inf, 3)

        if check_move(board, col):
            row = get_unvisited(board, col)
            fill_board(board, row, col, PLAYER_2)

            if check_win(board, PLAYER_2):
                label = myfont.render("Player 2 Menang.", 1, GOLD)
                board_screen.blit(label, (100, 10))
                game_over = True

            print_board(board)
            print("SCORE : " + str(score))
            draw_board(board)
            pygame.display.update()

            turn ^= 1

    if game_over:
        pygame.time.wait(2000)
