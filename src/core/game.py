
import pygame

from config import WIDTH, HEIGHT, FPS, WINDOW_TITLE
from src.core.states import MENU, PLAYING
from src.ui.menu import Menu
from src.board.board import Board


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)

        self.clock = pygame.time.Clock()
        self.running = True

        self.state = MENU

        self.menu = Menu(self.screen)
        self.board = None

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
                continue

            if self.state == MENU:
                self.menu.handle_event(event)

                if self.menu.exit_requested:
                    self.running = False

                elif self.menu.get_config() is not None:
                    self.start_game()

            elif self.state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.back_to_menu()
                        continue

    def start_game(self):
        config = self.menu.get_config()

        if config is None:
            return

        size = config["size"]
        infinite = config["infinite"]

        # Infinite hiện tại chỉ dùng kích thước tối đa,
        # chưa triển khai bàn cờ vô hạn.
        if size is None:
            size = 15

        self.board = Board(
            infinite = infinite,
            size = size
        )

        self.state = PLAYING

    def back_to_menu(self):
        self.board = None
        self.menu = Menu(self.screen)
        self.state = MENU

    def update(self, dt):
        if self.state == PLAYING and self.board is not None:
            self.board.update(dt)

    def draw(self):
        if self.state == MENU:
            self.menu.draw(self.screen)

        elif self.state == PLAYING:
            if self.board is not None:
                self.board.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()

