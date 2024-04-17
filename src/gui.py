import pygame
from src.constant import BLACK, BLUE, GREEN, ROWS, COLS, square_size, WHITE


class GUI:
    def __init__(self, window, game):
        self.window = window
        self.game = game
        self.selected_piece = (
            None  # Store the position (row, col) of the selected piece
        )
        self.valid_moves = {}  # Dictionary of valid moves from the selected position

    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                rect = (col * square_size, row * square_size, square_size, square_size)
                pygame.draw.rect(
                    self.window, WHITE if (row + col) % 2 == 0 else BLACK, rect
                )

                # Highlight the square if it is the selected piece or a valid move
                if self.selected_piece and (row, col) == self.selected_piece:
                    pygame.draw.rect(self.window, BLUE, rect)
                elif (row, col) in self.valid_moves:
                    pygame.draw.rect(self.window, GREEN, rect)

    def draw_pieces(self):
        board = self.game.get_board()  # Retrieve the board from the Game instance
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece:
                    piece.draw(self.window)

    def handle_click(self, row, col):
        if self.selected_piece:
            if (row, col) in self.valid_moves:
                if self.game.make_move(self.selected_piece, (row, col)):
                    self.deselect_piece()
            else:
                self.deselect_piece()
        else:
            self.select_piece(row, col)

    def select_piece(self, row, col):
        """Selects a piece and highlights its valid moves if it's the piece's turn."""
        piece = self.game.get_board()[row][col]
        print('current turn', self.game.get_current_turn())
        if piece is not None and piece.color == self.game.get_current_turn():
            self.selected_piece = (row, col)
            self.valid_moves = self.game.get_valid_moves(piece)
            print("Valid moves:", self.valid_moves)
        else:
            self.deselect_piece()

    def deselect_piece(self):
        """Deselects any selected piece."""
        self.selected_piece = None
        self.valid_moves = {}

    def draw(self):
        """Draws the entire game board including the board, pieces, and highlights."""
        self.draw_board()
        self.draw_pieces()
        pygame.display.update()
