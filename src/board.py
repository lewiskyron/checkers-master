from .piece import Piece, RED, BLACK_PIECES
from src.constant import ROWS, COLS


class Board:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.red_left = self.black_left = 12  # Assuming a standard game start
        self.red_kings = self.black_kings = 0
        self.initialize_pieces()

    def initialize_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 1:  # Only place pieces on black squares
                    if row < 3:
                        self.board[row][col] = Piece(row, col, RED)
                    elif row > 4:
                        self.board[row][col] = Piece(row, col, BLACK_PIECES)


    def place_piece(self, piece):
        """Place a piece on the board at its designated position."""
        row, col = piece.row, piece.col
        if (
            self.board[row][col] is None
        ):  # Ensure the cell is empty before placing the piece
            self.board[row][col] = piece
            if piece.color == RED:
                self.red_left += 1
                if piece.king:
                    self.red_kings += 1
            else:
                self.black_left += 1
                if piece.king:
                    self.black_kings += 1

    def get_board(self):
        return self.board

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_all_pieces(self):
        """Retrieve all pieces on the board."""
        pieces = []
        for row in self.board:
            for piece in row:
                if piece is not None:
                    pieces.append(piece)
        return pieces
    
    def evaluate(self):
        # Constants for weight
        PIECE_WEIGHT = 100
        KING_WEIGHT = 175
        CENTER_CONTROL_WEIGHT = 50
        KING_ROW_CONTROL_WEIGHT = 30
        BACK_ROW_DEFENSE_WEIGHT = 25
        MOBILITY_WEIGHT = 5
        POTENTIAL_KINGING_WEIGHT = 50

        # Basic piece and king counts with weighted scores
        piece_score = PIECE_WEIGHT * (self.black_left - self.red_left)
        king_score = KING_WEIGHT * (self.black_kings - self.red_kings)

        # Advanced scoring
        center_control = 0
        king_row_control = 0
        mobility_score = 0
        potential_kinging = 0
        back_row_defense = 0

        for piece in self.get_all_pieces():
            # Mobility: count valid moves
            valid_moves = self.get_valid_moves(piece)
            mobility_score += MOBILITY_WEIGHT * len(valid_moves)

            # Central control: extra points for pieces in the center
            if 2 <= piece.col <= 5 and 2 <= piece.row <= 5:
                center_control += CENTER_CONTROL_WEIGHT

            # Encouragement for pieces advancing to king rows
            if piece.color == BLACK_PIECES and not piece.king:
                if piece.row == ROWS - 2:  # One step away from becoming king
                    potential_kinging += POTENTIAL_KINGING_WEIGHT
                if piece.row == ROWS - 1:  # On the king row
                    king_row_control += KING_ROW_CONTROL_WEIGHT
            elif piece.color == RED and not piece.king:
                if piece.row == 1:  # One step away from becoming king
                    potential_kinging += POTENTIAL_KINGING_WEIGHT
                if piece.row == 0:  # On the king row
                    king_row_control += KING_ROW_CONTROL_WEIGHT

            # Back row defense
            if (piece.color == BLACK_PIECES and piece.row == 0) or \
            (piece.color == RED and piece.row == ROWS - 1):
                back_row_defense += BACK_ROW_DEFENSE_WEIGHT

        # Combine all scores into a final evaluation
        total_score = (piece_score + king_score + mobility_score +
                    center_control + king_row_control +
                    back_row_defense + potential_kinging)

        return total_score

    




    def get_pieces_by_color(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece is not None and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move_piece(self, piece, end_pos):
        """Move a piece from its current position to end_pos, handling king promotion and capturing."""
        if piece and end_pos in self.get_valid_moves(piece):
            # Swap positions on the board
            start_pos = (piece.row, piece.col)
            (
                self.board[start_pos[0]][start_pos[1]],
                self.board[end_pos[0]][end_pos[1]],
            ) = self.board[end_pos[0]][end_pos[1]], self.board[start_pos[0]][start_pos[1]]

            # Update the piece's position
            piece.move(end_pos[0], end_pos[1])

            # Check if the piece reaches the back rows for king promotion
            if end_pos[0] == ROWS - 1 or end_pos[0] == 0:
                piece.define_king()
                if piece.color == BLACK_PIECES:
                    self.black_kings += 1
                else:
                    self.red_kings += 1

    def remove(self, pieces):
        """Remove pieces from the board."""
        for piece in pieces:
            if piece != 0:
                self.board[piece.row][piece.col] = None
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.black_left -= 1

    def winner(self):
        """Determine if there is a winner based on remaining pieces."""
        if self.red_left <= 0:
            return BLACK_PIECES
        elif self.black_left <= 0:
            return RED
        return None

    def get_valid_moves(self, piece):
        """Get all valid moves for a selected piece based on simple moves and captures."""
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLACK_PIECES or piece.king:
            left_moves = moves.update(
                self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left)
            )
            right_moves = moves.update(
                self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right)
            )

        if piece.color == RED or piece.king:
            moves.update(
                self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left)
            )
            moves.update(
                self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right)
            )
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current is None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        next_row = max(r - 3, 0)
                    else:
                        next_row = min(r + 3, ROWS)
                    moves.update(
                        self._traverse_left(r + step, next_row, step, color, left - 1, skipped=last)
                    )
                    moves.update(
                        self._traverse_right(r + step, next_row, step, color, left + 1, skipped=last)
                    )
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current is None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        next_row = max(r - 3, 0)
                    else:
                        next_row = min(r + 3, ROWS)
                    moves.update(
                        self._traverse_left(r + step, next_row, step, color, right - 1, skipped=last)
                    )
                    moves.update(
                        self._traverse_right(r + step, next_row, step, color, right + 1, skipped=last)
                    )
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        return moves
