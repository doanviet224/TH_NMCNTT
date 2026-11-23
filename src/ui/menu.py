import pygame

try:
    from .buttons import Button   # package bth
    from . import board
except ImportError:
    from buttons import Button    # tui chạy trực tiếp để test
    import board

BG = (30, 36, 100)
WHITE = (255, 255, 255)
GREEN, BLUE, PINK, PURPLE = (84, 205, 92), (72, 122, 246), (246, 106, 180), (160, 98, 242)
RED, GRAY, ORANGE, YELLOW = (240, 74, 86), (96, 108, 200), (255, 150, 46), (255, 212, 62)

SIZE_MAX = 25
BACK = {"opponent": "start", "mode": "opponent", "custom": "mode"}
TITLE = {"opponent": "OPPONENT", "mode": "MODE", "custom": "CUSTOM"}
_fonts = {}


def font(size):
    if size not in _fonts:
        _fonts[size] = pygame.font.SysFont("arial", size, bold=True)
    return _fonts[size]


def make_button(x, y, w, h, text, color, size=28):
    """Tạo ảnh nút rồi đưa vào Button của Gia Khanh."""
    img = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(img, color, img.get_rect(), border_radius=14)
    label = font(size).render(text, True, WHITE)
    img.blit(label, label.get_rect(center=(w // 2, h // 2)))
    btn = Button(x, y, img, 1)
    btn.click = pygame.mouse.get_pressed()[0] == 1  # nút mới: phải nhả chuột rồi mới tính click
    return btn


def run_menu(screen=None, clock=None):
    """Trả về dict cấu hình {opponent, mode, size, win, first, infinite, block_ends} hoặc None nếu thoát."""
    pygame.init()
    screen = screen or pygame.display.set_mode((540, 720))
    pygame.display.set_caption("K-7")
    clock = clock or pygame.time.Clock()
    W = screen.get_width()
    cx = W // 2 - 150
    s = {"page": "start", "opp": "PVE", "size": 10, "win": 5, "inf": False, "block": False, "first": "black"}
    out = {}

    def go(page):
        s["page"] = page

    def pick_opp(who):
        s["opp"] = who
        go("mode")

    def finish(mode, size, win, first="black", inf=False, block=False):
        out["r"] = {"opponent": s["opp"], "mode": mode, "size": size, "win": win,
                    "first": first, "infinite": inf, "block_ends": block}

    def play_custom():
        inf = s["inf"]
        finish("custom", None if inf else s["size"], s["win"] if inf else min(s["win"], s["size"]),
               s["first"], inf, s["block"])

    def clamp_win():
        s["win"] = min(s["win"], SIZE_MAX if s["inf"] else s["size"])

    def change(key, d):
        if key == "size" and s["inf"]:
            return
        s[key] = max(4, min(SIZE_MAX, s[key] + d))
        clamp_win()

    def toggle(key):
        s[key] = not s[key]
        clamp_win()

    def build():
        """Trả về (danh sách (nút, hàm), danh sách chữ)."""
        page, labels = s["page"], []
        big = lambda y, text, color, fn: (make_button(cx, y, 300, 64, text, color), fn)
        if page == "start":
            labels = [("K-7", (W // 2, 200), 150)]
            items = [big(420, "START", GREEN, lambda: go("opponent")),
                     big(510, "EXIT", RED, lambda: out.update(r=None))]
        elif page == "opponent":
            items = [big(280, "PVE - vs Computer", BLUE, lambda: pick_opp("PVE")),
                     big(370, "PVP - 2 Players", PINK, lambda: pick_opp("PVP"))]
        elif page == "mode":
            items = [big(240, "TIC TAC TOE", GREEN, lambda: finish("tictactoe", 9, 3)),
                     big(330, "CLASSIC", BLUE, lambda: finish("classic", 15, 5)),
                     big(420, "CUSTOM", PURPLE, lambda: go("custom"))]
        else:  # custom
            items = []
            rows = [("Board size", "size"), ("Win in a row", "win")]
            for i, (name, key) in enumerate(rows):
                y = 170 + i * 70
                val = "INF" if key == "size" and s["inf"] else str(s[key])
                labels += [(name, (40, y + 25), 24, "midleft"), (val, (W - 120, y + 25), 28)]
                items += [(make_button(W - 210, y, 50, 50, "-", ORANGE), lambda k=key: change(k, -1)),
                          (make_button(W - 80, y, 50, 50, "+", GREEN), lambda k=key: change(k, 1))]
            for i, (name, key, text) in enumerate([("Infinite", "inf", s["inf"]), ("Block both ends", "block", s["block"])]):
                y = 310 + i * 70
                labels.append((name, (40, y + 25), 24, "midleft"))
                items.append((make_button(W - 210, y, 180, 50, "ON" if text else "OFF", GREEN if text else GRAY, 22),
                              lambda k=key: toggle(k)))
            labels.append(("First move", (40, 485), 24, "midleft"))
            items.append((make_button(W - 210, 460, 180, 50, s["first"].upper(), GRAY, 22),
                          lambda: s.update(first="white" if s["first"] == "black" else "black")))
            items.append(big(570, "PLAY", GREEN, play_custom))
        if page != "start":
            labels.append((TITLE[page], (W // 2, 90), 56))
            items.append((make_button(16, 16, 110, 44, "< BACK", GRAY, 20), lambda: go(BACK[page])))
        return items, labels

    buttons, labels = build()
    while "r" not in out:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return None
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                if s["page"] == "start":
                    return None
                go(BACK[s["page"]])
                buttons, labels = build()

        screen.fill(BG)
        for text, pos, size, *anchor in labels:
            img = font(size).render(text, True, YELLOW if size == 150 else WHITE)
            screen.blit(img, img.get_rect(**{(anchor[0] if anchor else "center"): pos}))
        fired = None
        for btn, fn in buttons:
            if btn.draw(screen) and fired is None:
                fired = fn
        if fired:
            fired()
            buttons, labels = build()
        pygame.display.flip()
    return out["r"]
def run_game(screen=None):
    """Menu -> chọn chế độ -> truyền cấu hình -> hết ván -> menu."""
    pygame.init()
    screen = screen or pygame.display.set_mode((board.WIDTH, board.HEIGHT))
    while True:
        cfg = run_menu(screen)
        if cfg is None:
            return
        board.run(screen, cfg)
if __name__ == "__main__":
    run_game()
    pygame.quit()
