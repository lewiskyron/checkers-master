import pygame
from src.gui import GUI, WIN, FPS
from  src.game import initialize_board 

def main():
    pygame.init()
    board = initialize_board()
    clock = pygame.time.Clock()
    run = True
    gui = GUI(WIN, board)

    while run:
        clock.tick(FPS)
        gui.draw()
        for event in pygame.event.get(): # checks if any events have happened at any time 
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

    pygame.quit()


if __name__ == "__main__":
    main()
