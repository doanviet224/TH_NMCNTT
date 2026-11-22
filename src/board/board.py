import sys
import pygame

WIDTH, HEIGHT = 1000, 800
FPS = 60

BG_COLOR = (62, 78, 150)
BOARD_COLOR = (30, 32, 80)
LINE_COLOR = (70, 76, 140)
TEXT_COLOR = (230, 232, 255)
RED_COLOR = (255, 80, 80)

SIZE = 15                                   # SIZE x SIZE cells
BOARD_MAX_PX = 650                          # The maximum size of the Board, adjust to be divisible by the cell size
CELL = BOARD_MAX_PX // SIZE                 # The size of each cell
BOARD_PX = CELL * SIZE                      # The real size of the Board, render with the real size that multiple with SIZE
BOARD_LEFT = (WIDTH - BOARD_PX) // 2        # Top-left corner
BOARD_TOP = (HEIGHT - BOARD_PX) // 2
# (0,0) ┌──────────────────────────────┐
#       │ 55                           │
#       │   (155,55)┌──────────┐       │
#       │           │   690²   │       │
#       │           └──────────┘       │
#       │ 55                           │
#       └──────────────────────────────┘ (1000,800)

def init_window():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Caro")
    return screen


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def pos_to_cell(pos):
    """(pos_x, pos_y) -> coordinates of the cell (row, col)"""
    mx, my = pos
    col = (mx - BOARD_LEFT) // CELL
    row = (my - BOARD_TOP) // CELL
    if 0 <= row < SIZE and 0 <= col < SIZE:
        return row, col
    return None


def draw_board(screen):
    pygame.draw.rect(screen, BOARD_COLOR, (BOARD_LEFT, BOARD_TOP, BOARD_PX, BOARD_PX))
    for i in range(SIZE + 1):
        x = BOARD_LEFT + i * CELL
        y = BOARD_TOP + i * CELL
        pygame.draw.line(screen, LINE_COLOR, (x, BOARD_TOP), (x, BOARD_TOP + BOARD_PX))
        pygame.draw.line(screen, LINE_COLOR, (BOARD_LEFT, y), (BOARD_LEFT + BOARD_PX, y))


# 2 lines of (x, y) & (pos_x, pos_y)
def draw_mouse_pos(screen, font):
    x, y = pygame.mouse.get_pos()
    text = font.render(f"({x}, {y})", True, TEXT_COLOR)
    screen.blit(text, text.get_rect(midright=(WIDTH - 10, HEIGHT // 2 - 20)))
def draw_cell_info(screen, font):
    cell = pos_to_cell(pygame.mouse.get_pos())
    if cell is None:
        label = "Cell: none"
    else:
        label = f"Cell: ({cell[0]}, {cell[1]})"
    text = font.render(label, True, RED_COLOR)
    screen.blit(text, text.get_rect(midright=(WIDTH - 10, HEIGHT // 2 + 20)))


def draw(screen, font):
    screen.fill(BG_COLOR)
    draw_board(screen)
    draw_mouse_pos(screen, font)
    draw_cell_info(screen, font)
    pygame.display.flip()


def main():
    screen = init_window()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)

    running = True
    while running:
        clock.tick(FPS)
        running = handle_events()
        draw(screen, font)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()