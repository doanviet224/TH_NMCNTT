import pygame


class Button:
    def __init__(self, text, width, height, pos, color, font=None, size_text=30,
                 shadow_color=None, border_radius=15, disable=False, elevate=6, disable_text=None, sound=None):
        self.original_y = pos[1]
        self.elevate = elevate
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = color
        self.bottom_rect = pygame.Rect(
            (pos[0], pos[1] + elevate), (width, height))
        self.click_area = pygame.Rect(
            (pos[0], pos[1]), (width, height + elevate))

        if font is None:
            self.font = pygame.font.Font(None, size_text)
        else:
            self.font = pygame.font.SysFont(font, size_text)

        self.disable = disable
        self.is_pressed = False
        self.border_radius = border_radius

        if shadow_color is None:
            self.shadow_color = tuple(int(c * 0.7) for c in color)
        else:
            self.shadow_color = shadow_color

        if disable_text is None:
            disable_text = text
        self.text_surf_normal = self.font.render(text, True, (255, 255, 255))
        self.text_surf_disable = self.font.render(
            disable_text, True, (145, 145, 145))
        is_hover = None
        self.is_hover = is_hover
        self.sound = sound

    def draw(self, surface):
        self.is_hover = self.click_area.collidepoint(pygame.mouse.get_pos())
        if self.disable:
            bg_color = (20, 50, 110)
            sh_color = (15, 35, 80)
            text_surf = self.text_surf_disable
        else:
            if self.is_hover:
                bg_color = tuple(min(255, c + 15) for c in self.top_color)
            else:
                bg_color = self.top_color
            sh_color = self.shadow_color
            text_surf = self.text_surf_normal

        if self.is_pressed and not self.disable:
            self.top_rect.y = self.original_y + self.elevate
        else:
            self.top_rect.y = self.original_y

        text_rect = text_surf.get_rect(center=self.top_rect.center)
            
        pygame.draw.rect(surface, sh_color, self.bottom_rect,
                         border_radius=self.border_radius)
        pygame.draw.rect(surface, bg_color, self.top_rect,
                         border_radius=self.border_radius)
        surface.blit(text_surf, text_rect)

    def is_click(self, event):
        if self.disable:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.click_area.collidepoint(event.pos):
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.is_pressed:
            self.is_pressed = False
            if self.click_area.collidepoint(event.pos):
                if self.sound:
                    self.sound.play()
                return True
        return False


class ToggleSwitch:
    def __init__(self, pos, width=96, height=44, is_on=False, font=None, sound = None):
        self.rect = pygame.Rect(pos, (width, height))
        self.is_on = is_on
        self.radius = height // 2

        self.anim_progress = 1.0 if is_on else 0.0

        self.on_color = (95, 215, 75)
        self.off_color = (35, 75, 150)
        self.knob_color = (255, 255, 255)
        self.sound = sound
        if font is None:
            self.font = pygame.font.Font(None, 24)
        else:
            self.font = pygame.font.SysFont(font, 20, bold=True)

        self.on_text = self.font.render("ON", True, (255, 255, 255))
        self.off_text = self.font.render("OFF", True, (185, 210, 255))

    def _lerp_color(self, c1, c2, t):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

    def draw(self, surface):
        target = 1.0 if self.is_on else 0.0
        self.anim_progress += (target - self.anim_progress) * 0.22
        if abs(target - self.anim_progress) < 0.01:
            self.anim_progress = target


        outer_rect = self.rect.inflate(4, 4)
        pygame.draw.rect(surface, (10, 30, 80), outer_rect,
                         border_radius=self.radius + 2)

        bg_color = self._lerp_color(
            self.off_color, self.on_color, self.anim_progress)
        pygame.draw.rect(surface, bg_color, self.rect,
                         border_radius=self.radius)

    
        border_col = tuple(min(255, c + 30) for c in bg_color)
        pygame.draw.rect(surface, border_col, self.rect,
                         width=2, border_radius=self.radius)

        
        knob_y = self.rect.centery
        if self.anim_progress > 0.5:
            text_rect = self.on_text.get_rect(
                center=(self.rect.x + self.rect.width * 0.30, knob_y))
            surface.blit(self.on_text, text_rect)
        else:
            text_rect = self.off_text.get_rect(
                center=(self.rect.x + self.rect.width * 0.68, knob_y))
            surface.blit(self.off_text, text_rect)

        
        padding = 5
        knob_radius = self.radius - padding
        left_x = self.rect.left + self.radius
        right_x = self.rect.right - self.radius
        knob_x = int(left_x + (right_x - left_x) * self.anim_progress)

      
        pygame.draw.circle(surface, (0, 0, 0, 80),
                           (knob_x, knob_y + 3), knob_radius)
        pygame.draw.circle(surface, (200, 210, 225),
                           (knob_x, knob_y + 2), knob_radius) 
        pygame.draw.circle(surface, self.knob_color,
                           (knob_x, knob_y), knob_radius)

    def is_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_on = not self.is_on
                if self.sound:
                    self.sound.play()
                return True
        return False

class OptionButton(Button):
    def __init__(self, text, pos, width=120, height=46, selected=False,
                 icon_color=None, font=None, size_text=24, elevate=5, sound = None):
        super().__init__(
            text=text,
            width=width,
            height=height,
            pos=pos,
            color=(30, 68, 150),         
            font=font,
            size_text=size_text,
            shadow_color=(15, 38, 95),   
            border_radius=12,
            elevate=elevate,
            sound = sound
        )
        self.selected = selected
        self.icon_color = icon_color
        self.selected_color = (42, 90, 185)     
        self.border_normal = (70, 115, 195)
        self.border_selected = (255, 215, 50)   

    def draw(self, surface):
        if self.is_pressed and not self.disable:
            self.top_rect.y = self.original_y + self.elevate
        else:
            self.top_rect.y = self.original_y
        
        is_hover = self.top_rect.collidepoint(pygame.mouse.get_pos())
        if self.selected:
            bg_color = self.selected_color
        elif is_hover:
            bg_color = tuple(min(255, c + 15) for c in self.top_color)
        else:
            bg_color = self.top_color

        
        pygame.draw.rect(surface, self.shadow_color, self.bottom_rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, bg_color, self.top_rect, border_radius=self.border_radius)

        
        if self.selected:
            pygame.draw.rect(surface, self.border_selected, self.top_rect, width=3, border_radius=self.border_radius)
        else:
            pygame.draw.rect(surface, self.border_normal, self.top_rect, width=2, border_radius=self.border_radius)

        
        if self.icon_color is not None:
            icon_x = self.top_rect.x + 24
            icon_y = self.top_rect.centery
            pygame.draw.circle(surface, (255, 255, 255), (icon_x, icon_y), 9)
            pygame.draw.circle(surface, self.icon_color, (icon_x, icon_y), 7)
            text_rect = self.text_surf_normal.get_rect(midleft=(icon_x + 15, icon_y))
        else:
            text_rect = self.text_surf_normal.get_rect(center=self.top_rect.center)

        surface.blit(self.text_surf_normal, text_rect)
''' Them nut switch va nut option, co the test cac nut bang cach undo code duoi day'''
# import sys
# pygame.mixer.init()
# pygame.init()
# SCREEN_WIDTH = 1000
# SCREEN_HEIGHT = 800

# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption('Button test')
# click_sound = pygame.mixer.Sound("game-start-sound-effect.mp3")
# click_sound.set_volume(0.5)
# normal_button = Button("click me", 150, 70,(500,500), (222, 57, 57), sound=click_sound)
# disable_button = Button("Not click me", 150, 70,(800,500), (57, 111, 222), sound=click_sound)
# # nut co ban text, width, height, pos, color
# infinite_switch = ToggleSwitch((400, 100), is_on=False, sound=click_sound)
# # khởi tạo switch (pos, is_on, font)
# Clock = pygame.time.Clock()
# fps = 60
# white_opt = OptionButton("White", (300, 200), selected=False, icon_color=(255, 255, 255), sound=click_sound)
# black_opt = OptionButton("Black", (430, 200), selected=True, icon_color=(20, 20, 20), sound=click_sound)
# # khởi tạo nút option (text, pos, selected, màu của chấm tròn)
# while True:
#     screen.fill((255,255,255))  #fill nền trắng
#     # vẽ các nút
#     normal_button.draw(screen)
#     disable_button.draw(screen)
#     infinite_switch.draw(screen)
#     white_opt.draw(screen)
#     black_opt.draw(screen)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         if normal_button.is_click(event):
#             disable_button.disable = not disable_button.disable
#         if disable_button.is_click(event):
#             print("click")
#         if infinite_switch.is_click(event):
#             print("Infinite:", infinite_switch.is_on)

#         if white_opt.is_click(event):
#             white_opt.selected = True
#             black_opt.selected = False
#         if black_opt.is_click(event):
#             black_opt.selected = True
#             white_opt.selected = False

#     pygame.display.update()
#     Clock.tick(fps)