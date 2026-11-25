
import pygame


class InputHandler:
    def __init__(self, board):
        self.board = board

    def clamp_camera(self):
        b = self.board
        real_px = b.real_cells * b.cell

        b.real_left = min(b.real_left, b.board_left)
        b.real_left = max(b.real_left, b.board_left + b.board_px - real_px)
        b.real_top = min(b.real_top, b.board_top)
        b.real_top = max(b.real_top, b.board_top + b.board_px - real_px)

    def move_camera(self, dt):
        b = self.board

        if not b.infinite:
            return

        keys = pygame.key.get_pressed()
        step = round(b.CAM_SPEED * dt)

        if keys[pygame.K_a]:
            b.real_left += step
        if keys[pygame.K_d]:
            b.real_left -= step
        if keys[pygame.K_w]:
            b.real_top += step
        if keys[pygame.K_s]:
            b.real_top -= step

        self.clamp_camera()

    def pos_to_cell(self, pos):
        return self.board.pos_to_cell(pos)

    def handle_event(self, event):
        b = self.board

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Kiểm tra click nút thoát
            if b.exit_button_rect.collidepoint(event.pos):
                b.exit_requested = True
                return

            cell = b.pos_to_cell(event.pos)
            if cell is not None:
                print(f"Clicked cell: {cell}")

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if b.infinite and b.pos_to_cell(event.pos) is not None:
                b.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            b.dragging = False

        elif event.type == pygame.MOUSEMOTION and b.dragging:
            if event.buttons[2]:
                b.real_left += event.rel[0]
                b.real_top += event.rel[1]
                self.clamp_camera()
            else:
                b.dragging = False

    def update(self, dt):
        self.move_camera(dt)
