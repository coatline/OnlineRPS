import pygame

font : pygame.font.Font
display : pygame.display 
width = 500
height = 500

def initialize():
    global font, display
    pygame.init()
    font = pygame.font.Font(None, 36)
    display = pygame.display.set_mode((width, height))

def display_text(custom_font : pygame.font.Font, text : str, text_color : tuple[float, float, float], rect : pygame.rect, surface : pygame.surface):
    text_surface = custom_font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def display_text(text : str, text_color : tuple[float, float, float], rect : pygame.rect, surface : pygame.surface):
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)