from copy import deepcopy
from src.constant import BLACK_PIECES, RED


def iterative_deepening_minimax(board, max_depth, game):
    best_move = None
    best_val = float("-inf") if game.get_current_turn() == BLACK_PIECES else float("inf")
    for depth in range(1, max_depth + 1):
        val, move = minimax(
            board,
            depth,
            float("-inf"),
            float("inf"),
            game.get_current_turn() == BLACK_PIECES,
            game,
            max_depth,
        )
        if (game.get_current_turn() == BLACK_PIECES and val > best_val) or (
            game.get_current_turn() != BLACK_PIECES and val < best_val
        ):
            best_val = val
            best_move = move
    return best_val, best_move


def minimax(board, depth, alpha, beta, is_maximizing_player, game, max_depth):
    if depth == 0 or board.winner() is not None:
        return board.evaluate(), None

    move_data = get_all_moves(
        board, BLACK_PIECES if is_maximizing_player else RED, game
    )
    best_move = None
    best_move_details = None

    if is_maximizing_player:
        max_eval = float("-inf")
        for new_board, move_details, _, move_key in move_data:
            evaluation, _ = minimax(
                new_board, depth - 1, alpha, beta, False, game, max_depth
            )
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = new_board
                best_move_details = move_key
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                if best_move_details:
                    update_history_score(game, best_move_details, depth, max_depth)
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for new_board, move_details, _, move_key in move_data:
            evaluation, _ = minimax(
                new_board, depth - 1, alpha, beta, True, game, max_depth
            )
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = new_board
                best_move_details = move_key
            beta = min(beta, evaluation)
            if beta <= alpha:
                if best_move_details:
                    update_history_score(game, best_move_details, depth, max_depth)
                break
        return min_eval, best_move


def get_all_moves(board, color, game):
    moves = []
    for piece in board.get_pieces_by_color(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skipped in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skipped)
            # Append both the new board and the move details
            move_details = (
                (piece.row, piece.col),
                move,
            )  # move is typically the end position
            move_key = (
                piece.row,
                piece.col,
                move[0],
                move[1],
            )  # Create a unique key for the move
            move_score = game.history_scores.get(move_key, 0)
            moves.append((new_board, move_details, move_score, move_key))
    # Sort based on the history heuristic score
    moves.sort(key=lambda x: x[2], reverse=True)
    return moves


def update_history_score(game, move_key, depth, max_depth):
    # Higher score increment for moves closer to the root
    depth_weight = max_depth - depth + 1
    game.history_scores[move_key] = game.history_scores.get(move_key, 0) + depth_weight


def decay_history_scores(game):
    decay_factor = 0.99  # Decay scores by 1%
    for key in game.history_scores:
        game.history_scores[key] *= decay_factor


def normalize_history_scores(game):
    max_score = max(game.history_scores.values(), default=1)  # Avoid division by zero
    for key in game.history_scores:
        game.history_scores[key] /= max_score


def simulate_move(piece, move, board, skipped):
    board.move_piece(piece, move)
    if skipped:
        board.remove(skipped)
    return board
