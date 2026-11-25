
import pygame


class Renderer:
    def __init__(self, board):
        self.board = board
        self.font = pygame.font.Font(None, 32)

    def draw_border(self, screen):
        b = self.board

        left = b.board_left - b.BORDER_PX
        top = b.board_top - b.BORDER_PX
        size = b.board_px + 2 * b.BORDER_PX

        pygame.draw.rect(screen, b.GOLD_COLOR, (left, top, size, size))

    def draw_board(self, screen):
        b = self.board

        pygame.draw.rect(
            screen,
            b.BOARD_COLOR,
            (b.board_left, b.board_top, b.board_px, b.board_px)
        )

        for i in range(b.real_cells + 1):
            x = b.real_left + i * b.cell
            y = b.real_top + i * b.cell

            if b.board_left <= x <= b.board_left + b.board_px:
                pygame.draw.line(
                    screen, b.LINE_COLOR,
                    (x, b.board_top),
                    (x, b.board_top + b.board_px)
                )

            if b.board_top <= y <= b.board_top + b.board_px:
                pygame.draw.line(
                    screen, b.LINE_COLOR,
                    (b.board_left, y),
                    (b.board_left + b.board_px, y)
                )

    def draw_mouse_pos(self, screen):
        b = self.board
        x, y = pygame.mouse.get_pos()

        text = self.font.render(f"({x}, {y})", True, b.TEXT_COLOR)
        screen.blit(
            text,
            text.get_rect(midright=(b.WIDTH - 10, b.HEIGHT // 2 - 20))
        )

    def draw_cell_info(self, screen):
        b = self.board
        cell = b.pos_to_cell(pygame.mouse.get_pos())

        if cell is None:
            label = "Cell: none"
        else:
            label = f"Cell: ({cell[0]}, {cell[1]})"

        text = self.font.render(label, True, b.RED_COLOR)
        screen.blit(
            text,
            text.get_rect(midright=(b.WIDTH - 10, b.HEIGHT // 2 + 20))
        )

    def draw_exit_button(self, screen):
        b = self.board
        mouse_pos = pygame.mouse.get_pos()

        if b.exit_button_rect.collidepoint(mouse_pos):
            color = (200, 50, 50)
        else:
            color = (150, 35, 35)

        pygame.draw.rect(
            screen,
            color,
            b.exit_button_rect,
            border_radius=5
        )

        text = self.font.render("X", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=b.exit_button_rect.center))

    def draw(self, screen):
        b = self.board

        screen.fill(b.BG_COLOR)

        self.draw_border(screen)
        self.draw_board(screen)
        self.draw_mouse_pos(screen)
        self.draw_cell_info(screen)
        self.draw_exit_button(screen)
