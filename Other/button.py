from utilities import * 
import pygame
import screen

class Button:
    def __init__(self, x, y, width, height, text, text_color, normal_color, hover_color, action, *args):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_color = text_color
        self.text = text

        self.current_color = normal_color
        self.normal_color = normal_color
        self.hover_color = hover_color
        
        self.is_active = True
        self.action = action
        self.args = args
        self.font = pygame.font.Font(None, 36)  # Font for button text
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect)
        screen.display_text(self.text, self.text_color, self.rect, surface=surface)
        # text_surface = self.font.render(self.text, True, self.text_color)
        # text_rect = text_surface.get_rect(center=self.rect.center)
        # surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if self.is_active == False:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action(*self.args)
                self.current_color = self.hover_color
        elif event.type == pygame.MOUSEMOTION and self.rect.collidepoint(event.pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.normal_color

    def set_active(self, b : bool):
        self.is_active = b

        if b == True:
            self.current_color = self.normal_color
        else:
            self.current_color = self.hover_color