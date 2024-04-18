from src.constant import BLACK_PIECES, RED

class AI_agent:
    def __init__(self, color, depth):
        self.color = color
        self.depth = depth

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.check_game_over():
            return self.evaluate(game.board), None

        best_move = None
        if maximizing_player:
            max_eval = float("-inf")
            ai_pieces = game.board.get_pieces_by_color(self.color)
            for piece in ai_pieces:
                current_valid_moves = game.board.get_valid_moves(piece)
                print(len(current_valid_moves))
                if not current_valid_moves:
                    continue
                for pos in current_valid_moves:
                    simulated_game = game.deep_copy()
                    simulated_game.board.move_piece(piece, pos)

                    eval = self.minimax(simulated_game, depth - 1, alpha, beta, False)[0]
                    if eval > max_eval:
                        max_eval = eval
                        best_move = ((piece.row, piece.col), pos)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval, best_move
        else:
            min_eval = float("inf")
            opponent_color = RED if self.color == BLACK_PIECES else BLACK_PIECES
            for piece in game.board.get_pieces_by_color(opponent_color):
                current_opponent_valid_moves = game.board.get_valid_moves(piece)
                if not current_opponent_valid_moves:
                    continue
                for pos in current_opponent_valid_moves:
                    simulated_game = game.deep_copy()
                    simulated_game.board.move_piece(piece, pos)
                    eval = self.minimax(simulated_game, depth - 1, alpha, beta, True)[0]
                    if eval < min_eval:
                        min_eval = eval
                        best_move = ((piece.row, piece.col), pos)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval, best_move

    def evaluate(self, board):
        # Directly call the board's evaluate method
        return board.evaluate()

    def choose_move(self, game):
        _, best_move = self.minimax(
            game,
            self.depth,
            float("-inf"),
            float("inf"),
            self.color == game.get_current_turn(),
        )
        return best_move
