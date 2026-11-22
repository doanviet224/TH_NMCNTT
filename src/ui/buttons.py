import pygame
class Button:
    def __init__(self, x, y, img, scale):
        width = img.get_width()
        height = img.get_height()
        self.img = pygame.transform.scale(img,(int(width*scale), int(height*scale)))
        self.rect = self.img.get_rect()
        self.rect.topleft = (x,y)
        self.click = False
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if(self.rect.collidepoint(pos) == 1):
            if(pygame.mouse.get_pressed()[0] == 1 and self.click == False):
                self.click = True
                action = True
            if(pygame.mouse.get_pressed()[0] == 0):
                self.click = False
        surface.blit(self.img,(self.rect.x, self.rect.y))
        return action