
import pygame

from src.core.states import MENU, PLAYING, PAUSED, GAME_OVER
from config import WIDTH, HEIGHT, FPS, WINDOW_TITLE
from src.ui.menu import Menu
from src.board.board import Board
from src.board.renderer import Renderer




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
        self.match_config = None

    # ---------------- EVENTS ----------------

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.state == MENU:
                self.menu.handle_event(event)

                if self.menu.exit_requested:
                    self.running = False
                    return

            elif self.state == PLAYING:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.back_to_menu()
                        continue

                if self.board is not None:
                    self.board.handle_event(event)

            elif self.state == PAUSED:
                pass

            elif self.state == GAME_OVER:
                pass

        # Kiểm tra xem người chơi đã nhấn PLAY chưa
        if self.state == MENU:
            config = self.menu.get_config()

            if config is not None:
                self.start_game(config)

    # ---------------- GAME CONTROL ----------------

    def start_game(self, config):
        self.match_config = config

        self.board = Board(
            infinite=config["infinite"],
            size=config["size"]
        )

        self.state = PLAYING

    def back_to_menu(self):
        self.board = None
        self.match_config = None

        self.menu.reset()
        self.state = MENU

    # ---------------- UPDATE ----------------

    def update(self, dt):
        if self.state == MENU:
            self.menu.update(dt) if hasattr(self.menu, "update") else None

        elif self.state == PLAYING:
            if self.board is not None:
                self.board.update(dt)

    # ---------------- DRAW ----------------

    def draw(self):
        if self.state == MENU:
            self.menu.draw(self.screen)

        elif self.state == PLAYING:
            if self.board is not None:
                self.board.draw(self.screen)

        pygame.display.flip()

    # ---------------- MAIN LOOP ----------------

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
