
import pygame


class Renderer:
    def __init__(self, board):
        self.board = board
        self.font = pygame.font.Font(None, 32) # Font X/ O size
        self.xo_font = pygame.font.Font(None, board.cell_size)

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
            x = b.real_left + i * b.cell_size
            y = b.real_top + i * b.cell_size

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

    def draw_XO(self, screen, board_data):
        b = self.board

        clip_rect = pygame.Rect(b.board_left, b.board_top, b.board_px, b.board_px)
        screen.set_clip(clip_rect)

        cells = (
            board_data.items()
            if isinstance(board_data, dict)
            else (((r, c), val) for r, row in enumerate(board_data) for c, val in enumerate(row))
        )

        for (r, c), val in cells:
            if val == 0:
                continue

            (lx, ty), (rx, by) = b.cell_to_rect(r, c)

            # Kiểm tra ô có nằm trong khung hình không
            in_view = (rx > b.board_left and lx < b.board_left + b.board_px and
                       by > b.board_top  and ty < b.board_top  + b.board_px)

            if not in_view:
                continue

            label = "X" if val == 1 else "O"
            color = b.RED_COLOR if val == 1 else b.GOLD_COLOR

            cx, cy = b.cell_to_center(r, c)
            text = self.xo_font.render(label, True, color)
            screen.blit(text, text.get_rect(center=(cx, cy)))

        screen.set_clip(None)

    def draw(self, screen, board_data=None):
        b = self.board

        screen.fill(b.BG_COLOR)

        self.draw_border(screen)
        self.draw_board(screen)
        self.draw_mouse_pos(screen)
        self.draw_cell_info(screen)
        self.draw_exit_button(screen)

        if board_data is not None:
            self.draw_XO(screen, board_data)

        # if board_data is not None:
        #     non_zero = [
        #         (r, c, val)
        #         for r, row in enumerate(board_data)
        #         for c, val in enumerate(row)
        #         if val != 0
        #     ]
        #     print(non_zero)
