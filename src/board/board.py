
import os
import sys
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from config import WIDTH, HEIGHT, FPS
from src.board.input_handler import InputHandler
from src.ui.renderer import Renderer
from src.logic.game_logic import GameLogic


class Board:
    WIDTH = WIDTH
    HEIGHT = HEIGHT
    FPS = FPS

    BG_COLOR = (62, 78, 150)
    BOARD_COLOR = (30, 32, 80)
    LINE_COLOR = (70, 76, 140)
    TEXT_COLOR = (230, 232, 255)
    RED_COLOR = (255, 80, 80)
    GOLD_COLOR = (230, 180, 40)

    BORDER_PX = 10
    BOARD_MAX_PX = 650
    CAM_SPEED = 400

    def __init__(self, infinite, size, game_logic=None):
        self.infinite = infinite
        self.size = size
        self.game_logic = game_logic

        if self.infinite:
            self.real_cells = 100
            self.view_cells = 10.5
            self.start_row, self.start_col = 40, 40
        else:
            self.real_cells = self.size
            self.view_cells = self.size
            self.start_row, self.start_col = 0, 0

        self.cell_size = int(self.BOARD_MAX_PX // self.view_cells)
        self.board_px = int(self.cell_size * self.view_cells)

        self.board_left = (self.WIDTH - self.board_px) // 2
        self.board_top = (self.HEIGHT - self.board_px) // 2

        self.real_left = self.board_left - self.start_col * self.cell_size
        self.real_top = self.board_top - self.start_row * self.cell_size

        self.dragging = False

        self.input_handler = InputHandler(self)
        self.renderer = Renderer(self)

        self.exit_requested = False
        self.exit_button_rect = pygame.Rect(self.WIDTH - 55, 15, 40, 40)

    def pos_to_cell(self, pos):
        mx, my = pos

        if (self.board_left <= mx < self.board_left + self.board_px
                and self.board_top <= my < self.board_top + self.board_px):

            col = (mx - self.real_left) // self.cell_size
            row = (my - self.real_top) // self.cell_size

            return row, col

        return None

    def cell_to_rect(self, row, col):
        top_left     = (self.real_left + col * self.cell_size, self.real_top + row * self.cell_size)
        bottom_right = (top_left[0] + self.cell_size,          top_left[1] + self.cell_size)
        return top_left, bottom_right

    def cell_to_center(self, row, col):
        top_left, bottom_right = self.cell_to_rect(row, col)
        cx = (top_left[0] + bottom_right[0]) // 2
        cy = (top_left[1] + bottom_right[1]) // 2
        return cx, cy

    def handle_event(self, event):
        self.input_handler.handle_event(event)

    def update(self, dt):
        self.input_handler.update(dt)

    def draw(self, screen):
        board_data = self.game_logic.board if self.game_logic is not None else None
        self.renderer.draw(screen, board_data)

    def run_frame(self, screen, events, dt):
        for event in events:
            self.handle_event(event)

        self.update(dt)
        self.draw(screen)


def test_board():
    pygame.init()

    screen = pygame.display.set_mode((Board.WIDTH, Board.HEIGHT))
    pygame.display.set_caption("Caro - Test Board")

    clock = pygame.time.Clock()
    board = Board(infinite=True, size=15)
    board.game_logic = GameLogic(board.real_cells)

    running = True

    while running:
        dt = clock.tick(Board.FPS) / 1000
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        board.run_frame(screen, events, dt)
        if board.exit_requested:
            running = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    test_board()
