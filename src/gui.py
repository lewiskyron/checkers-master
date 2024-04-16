import pygame 

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
square_size = WIDTH // COLS

# RGB color definitions with a more realistic tone
WHITE = (240, 217, 181)  # A light wooden color for one set of squares
BLACK = (181, 136, 99)   # A dark wooden color for the other set of squares
RED = (194, 59, 34)      # A rich, dark red for one set of game pieces
GREEN = (0, 100, 0)      # A deep green for potential highlighting of moves or selected piece
BLACK_PIECES = (90, 90, 90)  # A lighter grey for the other set of game pieces
BLUE = (29, 77, 142)     # A deep blue, perhaps for highlighting last move or selection


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
FPS = 60

class GUI:
    def __init__(self, window, board):
        self.window = window
        self.board = board

    def draw_board(self):
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                rect = (col * square_size, row * square_size, square_size, square_size)
                pygame.draw.rect(
                    self.window, WHITE if (row + col) % 2 == 0 else BLACK, rect
                )

    def draw_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    piece.draw(self.window)

    def draw(self):
        self.draw_board()
        self.draw_pieces()
        pygame.display.update()
