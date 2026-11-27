import pygame

try:
    from .buttons import Button, ToggleSwitch, OptionButton   # chạy trong package
except ImportError:
    from buttons import Button, ToggleSwitch, OptionButton    # tui chạy trực tiếp để test

BG, WHITE, YELLOW = (30, 36, 100), (255, 255, 255), (255, 212, 62)
GREEN, BLUE, PINK, PURPLE = (84, 205, 92), (72, 122, 246), (246, 106, 180), (160, 98, 242)
RED, GRAY, ORANGE = (240, 74, 86), (96, 108, 200), (255, 150, 46)

SIZE_MIN, SIZE_MAX, WIN_MIN = 4, 25, 3
BACK = {"opponent": "start", "names": "opponent", "mode": "names", "custom": "mode"}
NAME_MAX = 12   # số ký tự tối đa của tên
CLICK_SOUND = "game-start-sound-effect.mp3"   # âm thanh click lấy từ buttons.py


class Menu:
    """Chuyển trang, lưu lựa chọn của player, đưa cấu hình cho game.py qua get_config()."""

    def __init__(self, screen):
        self.W = screen.get_width()
        self.exit_requested = False
        self._config = None
        self._fonts = {}
        self.click_sound = self._load_sound(CLICK_SOUND)

        # lựa chọn của player
        self.opponent, self.size, self.win = "PVE", 10, 5
        self.infinite = self.block_ends = False
        self.first = "black"
        self.names, self.active = ["", ""], 0   # tên đang gõ và ô đang chọn

        self.go("start")

    # ---------- API cho game.py ----------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return self.back()
        if self.page == "names" and self._handle_typing(event):
            return
        for widget, action in self.items:
            if widget.is_click(event):
                action()
                break  # trang có thể đã đổi

    def draw(self, screen):
        screen.fill(BG)
        for text, pos, size, anchor in self._labels():
            img = self._font(size).render(text, True, YELLOW if size > 100 else WHITE)
            screen.blit(img, img.get_rect(**{anchor: pos}))
        if self.page == "names":
            self._draw_names(screen)
        for widget, _ in self.items:
            widget.draw(screen)

    def get_config(self):
        return self._config

    def reset(self):
        self._config, self.exit_requested = None, False
        self.go("start")

    # ---------- Chuyển trang / lưu lựa chọn ----------
    def go(self, page):
        self.page = page
        if page == "names":
            pygame.key.start_text_input()   # cho phép gõ chữ (kể cả có dấu)
            self.active = 0
        else:
            pygame.key.stop_text_input()
        self._build()

    def back(self):
        if self.page == "start":
            self.exit_requested = True
        else:
            self.go(BACK[self.page])

    def pick_opponent(self, who):
        self.opponent = who
        self.go("names")

    def finish(self, mode, size, win):
        name1, name2 = self._final_names()
        self._config = {"opponent": self.opponent, "name1": name1, "name2": name2, "mode": mode, "size": size, "win": win,
                        "first": self.first, "infinite": self.infinite and mode == "custom",
                        "block_ends": self.block_ends and mode == "custom"}

    def change(self, key, delta):
        if key == "size":
            if self.infinite:
                return
            self.size = max(SIZE_MIN, min(SIZE_MAX, self.size + delta))
        else:
            self.win += delta
        self._clamp()

    def set_option(self, key, value):
        setattr(self, key, value)
        self._clamp()
        self._sync()

    def play_custom(self):
        self.finish("custom", None if self.infinite else self.size, self.win)

    # ---------- Nội bộ ----------
    def _clamp(self):
        self.win = max(WIN_MIN, min(self.win, SIZE_MAX if self.infinite else self.size))

    def _sync(self):
        for b in self.size_btns:
            b.disable = self.infinite
        for name, b in self.first_btns.items():
            b.selected = self.first == name

    @staticmethod
    def _load_sound(path):
        """Nạp âm thanh click"""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            sound = pygame.mixer.Sound(path)
            sound.set_volume(0.5)
            return sound
        except (pygame.error, FileNotFoundError):
            return None

    # ---------- Nhập tên ----------
    def _boxes(self):
        """Các ô nhập tên của trang names: PVE 1 ô, PVP 2 ô."""
        x = self.W // 2 - 170
        ys = [270] if self.opponent == "PVE" else [230, 350]
        return [pygame.Rect(x, y, 340, 52) for y in ys]

    def _final_names(self):
        """(tên người chơi 1, tên người chơi 2); để trống thì dùng tên mặc định."""
        pve = self.opponent == "PVE"
        name1 = self.names[0].strip() or ("You" if pve else "Player 1")
        name2 = "Computer" if pve else (self.names[1].strip() or "Player 2")
        return name1, name2

    def _handle_typing(self, event):
        """Xử lý gõ chữ / chọn ô ở trang names. Trả về True nếu event đã được dùng."""
        boxes = self._boxes()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(boxes):
                if rect.collidepoint(event.pos):
                    self.active = i
                    return True
        elif event.type == pygame.TEXTINPUT:
            text = "".join(c for c in event.text if c.isprintable())
            self.names[self.active] = (self.names[self.active] + text)[:NAME_MAX]
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.names[self.active] = self.names[self.active][:-1]
                return True
            if event.key == pygame.K_TAB:
                self.active = (self.active + 1) % len(boxes)
                return True
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if self.active < len(boxes) - 1:
                    self.active += 1
                else:
                    self.go("mode")
                return True
        return False

    def _draw_names(self, screen):
        hints = self._final_names_hint()
        for i, rect in enumerate(self._boxes()):
            pygame.draw.rect(screen, (20, 24, 70), rect, border_radius=12)
            border = YELLOW if i == self.active else GRAY
            pygame.draw.rect(screen, border, rect, width=3, border_radius=12)
            text = self.names[i]
            img = self._font(28).render(text or hints[i], True, WHITE if text else GRAY)
            screen.blit(img, img.get_rect(midleft=(rect.x + 14, rect.centery)))
            if i == self.active and (pygame.time.get_ticks() // 500) % 2 == 0:
                cx = rect.x + 14 + (img.get_width() if text else 0) + 2
                pygame.draw.line(screen, WHITE, (cx, rect.y + 12), (cx, rect.bottom - 12), 2)

    def _final_names_hint(self):
        """Chữ gợi ý (tên mặc định) hiện mờ trong ô còn trống."""
        return ("You",) if self.opponent == "PVE" else ("Player 1", "Player 2")

    def _font(self, size):
        if size not in self._fonts:
            self._fonts[size] = pygame.font.SysFont("TimesNewRoman", size, bold=True)
        return self._fonts[size]

    def _build(self):
        W, items, snd = self.W, [], self.click_sound
        self.size_btns, self.first_btns = [], {}

        def big(y, text, color, fn):
            items.append((Button(text, 300, 64, (W // 2 - 150, y), color, size_text=32, sound=snd), fn))

        def step(y, key):
            minus = Button("-", 50, 50, (W - 210, y), ORANGE, size_text=36, sound=snd)
            plus = Button("+", 50, 50, (W - 80, y), GREEN, size_text=36, sound=snd)
            items.extend([(minus, lambda: self.change(key, -1)), (plus, lambda: self.change(key, 1))])
            return [minus, plus]

        def switch(y, key):
            sw = ToggleSwitch((W - 140, y), is_on=getattr(self, key), sound=snd)
            items.append((sw, lambda: self.set_option(key, sw.is_on)))

        if self.page == "start":
            big(420, "START", GREEN, lambda: self.go("opponent"))
            big(510, "EXIT", RED, lambda: setattr(self, "exit_requested", True))

        elif self.page == "opponent":
            big(280, "PVE - vs Computer", BLUE, lambda: self.pick_opponent("PVE"))
            big(370, "PVP - 2 Players", PINK, lambda: self.pick_opponent("PVP"))

        elif self.page == "names":
            big(520, "NEXT", GREEN, lambda: self.go("mode"))

        elif self.page == "mode":
            big(240, "TIC TAC TOE", GREEN, lambda: self.finish("tictactoe", 3, 3))
            big(330, "CLASSIC", BLUE, lambda: self.finish("classic", 15, 5))
            big(420, "CUSTOM", PURPLE, lambda: self.go("custom"))

        else:  # custom
            self.size_btns = step(170, "size")
            step(240, "win")
            switch(316, "infinite")
            switch(386, "block_ends")
            for i, (name, color) in enumerate([("black", (20, 20, 20)), ("white", WHITE)]):
                opt = OptionButton(name.capitalize(), (W - 270 + i * 130, 460), icon_color=color, sound=snd)
                self.first_btns[name] = opt
                items.append((opt, lambda n=name: self.set_option("first", n)))
            big(570, "PLAY", GREEN, self.play_custom)

        if self.page != "start":
            items.append((Button("< BACK", 110, 44, (16, 16), GRAY, size_text=24, sound=snd), self.back))

        self.items = items
        self._sync()

    def _labels(self):
        W = self.W
        if self.page == "start":
            return [("K-7", (W // 2, 200), 150, "center")]
        labels = [(self.page.upper(), (W // 2, 90), 56, "center")]
        if self.page == "names":
            rows = [("Your name (X)", 242)] if self.opponent == "PVE" else \
                   [("Player 1 (X)", 202), ("Player 2 (O)", 322)]
            labels += [(t, (W // 2 - 170, y), 24, "midleft") for t, y in rows]
        if self.page == "custom":
            rows = [("Board size", 195), ("Win in a row", 265), ("Infinite", 338),
                    ("Block both ends", 408), ("First move", 483)]
            labels += [(name, (40, y), 24, "midleft") for name, y in rows]
            labels += [("INF" if self.infinite else str(self.size), (W - 120, 195), 28, "center"),
                       (str(self.win), (W - 120, 265), 28, "center")]
        return labels


if __name__ == "__main__":
    pygame.init()
    scr = pygame.display.set_mode((540, 720))
    clock, running = pygame.time.Clock(), True
    menu = Menu(scr)
    while running:
        clock.tick(60)
        for ev in pygame.event.get():
            running = running and ev.type != pygame.QUIT
            menu.handle_event(ev)
        if menu.exit_requested:
            running = False
        elif menu.get_config():
            print("Cấu hình:", menu.get_config())
            menu.reset()
        menu.draw(scr)
        pygame.display.flip()
    pygame.quit()
