from .board import Board
from src.constant import RED, BLACK_PIECES


class Game:
    def __init__(self):
        self.board = Board()  # Initialize the board
        self.turn = RED

    def get_board(self):
        """Return the current state of the board."""
        return self.board.get_board()

    def get_current_turn(self):
        """Returns the current player's turn."""
        return self.turn

    def change_turn(self):
        """Switch turns between players."""
        print('changint turns')
        if self.turn == BLACK_PIECES:
            self.turn = RED
        else:
            self.turn = RED

    def make_move(self, start_pos, end_pos):
        """
        Attempt to make a move on the board and update game state accordingly.
        """
        piece = self.board.get_board()[start_pos[0]][start_pos[1]]
        if (piece and piece.color == self.turn):
            valid_moves = self.board.get_valid_moves(piece)
            if end_pos in valid_moves:
                captured_positions = valid_moves[end_pos]
                self.board.move_piece(piece, end_pos)
                # self.board.remove(captured_positions)
                self.change_turn()
                self.check_game_over()
            return True
        return False

    def check_game_over(self):
        """
        Check if the game has ended and set the winner if there is one.
        """
        self.winner = self.board.winner()
        if self.winner is not None:
            print(f"Game Over! Winner: {self.winner}")

    def get_valid_moves(self, piece):
        """
        Retrieve all valid moves for the specified piece based on the current board state.
        """
        return self.board.get_valid_moves(piece)
