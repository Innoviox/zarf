import pygame
from word_solve import board_of, solve

pygame.init()

screen = pygame.display.set_mode((500, 500), 0, 32)

font = pygame.font.SysFont(None, 48)

class Board:
    def __init__(self, board):
        self.board = board_of(board)
        print(solve(self.board))


