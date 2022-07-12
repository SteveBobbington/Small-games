import pygame
import sys

class Button:
    def __init__(self, rect, command, text):
        self.font=pygame.font.SysFont("DTM-Mono", 24)
        self.font_colour=pygame.Color("white")
        self.rect=pygame.Rect(rect)
        self.image=pygame.Surface(self.rect.size).convert()
        self.function=command
        self.text=text
        self.text=self.font.render(self.text, True, self.font_colour)
        self.text_rect=self.text.get_rect(center=self.rect.center)

    def is_pressed(self):
        click=pygame.mouse.get_pressed()
        if click[0]==1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.function()
             
    def is_hovered(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True

    def draw(self, screen):
        if self.is_hovered():
            self.image=pygame.image.load("pictures/pressed button.png")
            self.image=pygame.transform.scale(self.image, (self.rect[2], self.rect[3]))
        else:
            self.image=pygame.image.load("pictures/button.png")
            self.image=pygame.transform.scale(self.image, (self.rect[2], self.rect[3]))
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

def draw_buttons(buttons, screen):
    for button in buttons:
        button.draw(screen)

def button_quit():
    pygame.display.quit()
    pygame.quit()
    sys.exit()
    
