import pygame
from src.constant import FPS
from src.game import Game
from src.constant import WIDTH, HEIGHT, square_size
from src.gui import GUI

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

    while run:
        for event in pygame.event.get():  # checks if any events have happened at any time
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = mouse_postion(pos)
                gui.handle_click(row, col)

        gui.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
