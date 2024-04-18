from .board import Board
from src.constant import RED, BLACK_PIECES
from src.agent import iterative_deepening_minimax


class Game:
    def __init__(self):
        self.board = Board()  # Initialize the board
        self.turn = RED
        self.ai_color = BLACK_PIECES
        self.history_scores = {}

        # self.ai_agent = AI_agent(BLACK_PIECES, 3)

    def get_board(self):
        """Return the current state of the board."""
        return self.board.get_board()

    def get_current_turn(self):
        """Returns the current player's turn."""
        return self.turn

    def change_turn(self):
        """Switch turns between players."""

        if self.turn == RED:
            self.turn = BLACK_PIECES
        elif self.turn == BLACK_PIECES:  # Use elif to ensure this is only evaluated if the first condition fails
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
                self.board.remove(captured_positions)
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
            return True
        return False

    def get_valid_moves(self, piece):
        """
        Retrieve all valid moves for the specified piece based on the current board state.
        """
        return self.board.get_valid_moves(piece)

    def agent_move(self):
        if self.turn == BLACK_PIECES:
            _, best_move = iterative_deepening_minimax(self.board, 5, self)
            if best_move:
                self.board = best_move
                self.change_turn()
