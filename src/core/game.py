import pygame

from config import WIDTH, HEIGHT, FPS, WINDOW_TITLE, WHITE
from src.core.states import MENU, PLAYING

from src.ui.menu import draw_menu, handle_menu_event
from src.board.board import draw_board

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)

        self.clock = pygame.time.Clock()
        self.running = True
        self.state = MENU

    def change_state(self, new_state):
        self.state = new_state

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif self.state == MENU:
                if handle_menu_event(event):
                    self.change_state(PLAYING)

            elif self.state == PLAYING:
                pass

    def draw(self):
        self.screen.fill(WHITE)

        if self.state == MENU: 
            draw_menu(self.screen)

        elif self.state == PLAYING:
            draw_board(self.screen)

    pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()