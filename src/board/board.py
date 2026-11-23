import os
import sys
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from config import WIDTH, HEIGHT, FPS

class Board:
    # Lấy giá trị trực tiếp từ config.py (không gán cứng số ở đây nữa)
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

    def __init__(self, infinite, size):
        self.infinite = infinite
        self.size = size

        if self.infinite:
            self.real_cells = 100
            self.view_cells = 10.5
            self.start_row, self.start_col = 40, 40
        else:
            self.real_cells = self.size
            self.view_cells = self.size
            self.start_row, self.start_col = 0, 0

        self.cell = int(self.BOARD_MAX_PX // self.view_cells)
        self.board_px = int(self.cell * self.view_cells)

        self.board_left = (self.WIDTH - self.board_px) // 2
        self.board_top = (self.HEIGHT - self.board_px) // 2

        self.real_left = self.board_left - self.start_col * self.cell
        self.real_top = self.board_top - self.start_row * self.cell

        self.font = pygame.font.Font(None, 32)

        self.dragging = False

    def clamp_camera(self):
        real_px = self.real_cells * self.cell

        self.real_left = min(self.real_left, self.board_left)
        self.real_left = max(self.real_left, self.board_left + self.board_px - real_px)
        self.real_top = min(self.real_top, self.board_top)
        self.real_top = max(self.real_top, self.board_top + self.board_px - real_px)

    def move_camera(self, dt):
        if not self.infinite:
            return

        keys = pygame.key.get_pressed()
        step = round(self.CAM_SPEED * dt)

        if keys[pygame.K_a]:
            self.real_left += step
        if keys[pygame.K_d]:
            self.real_left -= step
        if keys[pygame.K_w]:
            self.real_top += step
        if keys[pygame.K_s]:
            self.real_top -= step

        self.clamp_camera()

    def pos_to_cell(self, pos):
        mx, my = pos

        if (self.board_left <= mx < self.board_left + self.board_px
            and self.board_top <= my < self.board_top + self.board_px):

            col = (mx - self.real_left) // self.cell
            row = (my - self.real_top) // self.cell

            return row, col

        return None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cell = self.pos_to_cell(event.pos)

            if cell is not None:
                print(f"Clicked cell: {cell}")

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if self.infinite and self.pos_to_cell(event.pos) is not None:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            if event.buttons[2]:
                self.real_left += event.rel[0]
                self.real_top += event.rel[1]
                self.clamp_camera()
            else:
                self.dragging = False

    def update(self, dt):
        self.move_camera(dt)

    def draw_border(self, screen):
        left = self.board_left - self.BORDER_PX
        top = self.board_top - self.BORDER_PX
        size = self.board_px + 2 * self.BORDER_PX

        pygame.draw.rect(screen, self.GOLD_COLOR, (left, top, size, size))

    def draw_board(self, screen):
        pygame.draw.rect(
            screen,
            self.BOARD_COLOR,
            (self.board_left, self.board_top, self.board_px, self.board_px)
        )

        for i in range(self.real_cells + 1):
            x = self.real_left + i * self.cell
            y = self.real_top + i * self.cell

            if self.board_left <= x <= self.board_left + self.board_px:
                pygame.draw.line(
                    screen, self.LINE_COLOR,
                    (x, self.board_top),
                    (x, self.board_top + self.board_px)
                )

            if self.board_top <= y <= self.board_top + self.board_px:
                pygame.draw.line(
                    screen, self.LINE_COLOR,
                    (self.board_left, y),
                    (self.board_left + self.board_px, y)
                )

    def draw_mouse_pos(self, screen):
        x, y = pygame.mouse.get_pos()

        text = self.font.render(f"({x}, {y})", True, self.TEXT_COLOR)
        screen.blit(
            text,
            text.get_rect(midright=(self.WIDTH - 10, self.HEIGHT // 2 - 20))
        )

    def draw_cell_info(self, screen):
        cell = self.pos_to_cell(pygame.mouse.get_pos())

        if cell is None:
            label = "Cell: none"
        else:
            label = f"Cell: ({cell[0]}, {cell[1]})"

        text = self.font.render(label, True, self.RED_COLOR)
        screen.blit(
            text,
            text.get_rect(midright=(self.WIDTH - 10, self.HEIGHT // 2 + 20))
        )

    def draw(self, screen):
        screen.fill(self.BG_COLOR)

        self.draw_border(screen)
        self.draw_board(screen)
        self.draw_mouse_pos(screen)
        self.draw_cell_info(screen)

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

    running = True

    while running:
        dt = clock.tick(Board.FPS) / 1000
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        board.run_frame(screen, events, dt)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    test_board()