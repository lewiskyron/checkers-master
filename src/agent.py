from copy import deepcopy
from src.constant import BLACK_PIECES, RED


def minimax(board, depth, is_maximizing_player, game):
    if depth == 0 or board.winner() is not None:
        return board.evaluate(), board

    if is_maximizing_player:
        max_eval = float("-inf")
        best_move = None
        for move in get_all_moves(board, BLACK_PIECES, game):
            evaluation, _ = minimax(move, depth - 1, False, game)
            print(evaluation)
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float("inf")
        best_move = None
        for move in get_all_moves(board, RED, game):
            evaluation, _ = minimax(move, depth - 1, True, game)
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            
        print(min_eval, best_move)
        return min_eval, best_move


def get_all_moves(board, color, game):
    moves = []
    for piece in board.get_pieces_by_color(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skipped in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skipped)
            moves.append(new_board)
    return moves


def simulate_move(piece, move, board, skipped):
    board.move_piece(piece, move)
    if skipped:
        board.remove(skipped)
    return board
