from .constant import RED, BLACK_PIECES, square_size
import pygame


crown = pygame.transform.scale(pygame.image.load("assets/crown.png"), (45, 25))

class Piece: 
    def __init__(self,row,col,color):
        self.row = row
        self.color = color
        self.col = col
        self.king = False

        if self.color == RED:
            self.direction = -1
        else:
            self.direction = 1

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = square_size * self.col + square_size // 2
        self.y = square_size * self.row + square_size // 2

    def move(self, new_row, new_col):
        print('This is the new row and col', new_row, new_col)
        self.row = new_row
        self.col = new_col
        self.calc_pos()

    def define_king(self):
        self.king = True

    def draw(self, win):
        radius = square_size // 2 - 10
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(crown, (self.x - crown.get_width() // 2, self.y - crown.get_height() // 2))
