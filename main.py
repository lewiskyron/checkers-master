import pygame
from src.constant import FPS, BLACK_PIECES
from src.game import Game
from src.constant import WIDTH, HEIGHT, square_size
from src.gui import GUI
from src.ai import AI_agent

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

def mouse_postion(pos):
    x, y = pos
    row = y // square_size
    col = x // square_size
    return row, col


def main():
    pygame.init()
    game = Game()
    clock = pygame.time.Clock()
    run = True
    gui = GUI(WIN, game)
    ai_agent = AI_agent(BLACK_PIECES, 3)

    while run:

        for event in pygame.event.get():  # checks if any events have happened at any time
            if event.type == pygame.QUIT:
                run = False
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                # and game.get_current_turn() != ai_agent.color
            ):
                pos = pygame.mouse.get_pos()
                row, col = mouse_postion(pos)
                gui.handle_click(row, col)

        if game.turn == game.ai_color:
            game.agent_move()
            pygame.time.delay(1000)  # Add a delay to make AI moves observable

        if game.check_game_over():
            run = False

        gui.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
