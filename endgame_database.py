import itertools
import numpy as np
import sqlite3
from joblib import Parallel, delayed
from src.piece import Piece
from src.board import Board


# Define constants
RED, BLACK= "R", "B"
KING, MAN = "K", "M"
EMPTY = None
ROWS, COLS = 8, 8  # Assuming an 8x8 checkers board

# Dummy imports - replace with actual imports from your project structure
# from .board import Board
# from .piece import Piece, RED, BLACK_PIECES


class Piece:
    def __init__(self, row, col, color, king=False):
        self.row = row
        self.col = col
        self.color = color
        self.king = king
        print(
            f"Initialized {self.color} piece at ({self.row}, {self.col}), King: {self.king}"
        )

    def make_king(self):
        self.king = True
        print(f"Piece at ({self.row}, {self.col}) promoted to King.")


class Board:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.red_left = self.black_left = 12  # Assuming a standard game start
        self.red_kings = self.black_kings = 0
        self.initialize_pieces()

    def clear_board(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]

    def place_piece(self, piece):
        self.board[piece.row][piece.col] = piece

    def evaluate(self):
        # Calculate basic piece and king counts with weighted scores
        piece_score = 0.1 * (
            self.black_left - self.red_left
        )  # Adjust weight for simple piece count
        king_score = 2 * (
            self.black_kings - self.red_kings
        )  # Increased weight for kings

        # Positional and mobility scoring
        positional_score = 0
        mobility_score = 0
        for piece in self.get_all_pieces():
            if piece.king:
                # King positional advantage based on advancement
                positional_score += (
                    piece.row * 0.1
                    if piece.color == BLACK
                    else (ROWS - 1 - piece.row) * 0.1
                )
            else:
                # Mobility score calculated from valid moves available
                mobility_score += len(self.get_valid_moves(piece))

            # Central control bonus for being in the middle of the board
            if 2 <= piece.col <= 5 and 2 <= piece.row <= 5:
                positional_score += 0.2  # More for center pieces

        # Encourage maintaining pieces in the back row as a form of defense
        back_row_defense = 0
        for row in [0, ROWS - 1]:  # Assuming an 8-row board, adjust if different
            for col in range(COLS):  # Assuming an 8-column board
                piece = self.get_piece(row, col)
                if piece and piece.color == BLACK and row == 0:
                    back_row_defense += 0.5
                elif piece and piece.color == RED and row == ROWS - 1:
                    back_row_defense += 0.5

        # Combine all scores into a final evaluation
        total_score = (
            piece_score
            + king_score
            + positional_score
            + mobility_score
            + back_row_defense
        )
        return total_score


def setup_specific_board(board, positions, types, colors):
    board.clear_board()
    for pos, type_, color in zip(positions, types, colors):
        row, col = divmod(pos, COLS)
        piece = Piece(row, col, color, king=(type_ == KING))
        board.place_piece(piece)
    return board


def generate_and_analyze_configurations():
    all_positions = list(itertools.combinations(range(ROWS * COLS), 6))
    all_types = list(itertools.product([MAN, KING], repeat=6))
    all_colors = list(itertools.product([RED, BLACK], repeat=6))

    def process_configuration(positions, types, colors):
        board = Board()
        setup_specific_board(board, positions, types, colors)
        outcome = board.evaluate()
        board_state = np.array(
            [[p.color if p else EMPTY for p in row] for row in board.board]
        )
        return board_state.tobytes(), outcome

    results = Parallel(n_jobs=-1)(
        delayed(process_configuration)(pos, types, cols)
        for pos, types, cols in itertools.product(all_positions, all_types, all_colors)
    )
    return results


def store_results(db_path, data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS endgames
           (id INTEGER PRIMARY KEY, board_state BLOB, outcome TEXT)"""
    )
    cursor.executemany(
        "INSERT INTO endgames (board_state, outcome) VALUES (?, ?)", data
    )
    conn.commit()
    conn.close()


def endgame():
    db_path = "endgames.db"
    results = generate_and_analyze_configurations()
    store_results(db_path, results)
    print("Endgame tablebase generation complete.")

if __name__ == "__main__":
    endgame()
