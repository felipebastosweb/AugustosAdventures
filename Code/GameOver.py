import importlib
import pygame
from Settings import *
import os


# This is for file (images specifically) importing (This line changes the directory to where the project is saved)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

"""
 Mouse Graphic Engine
"""
class MouseCursor:
    def __init__(self):
        self.image = pygame.image.load(cursor_image)  # Carregue a imagem do cursor
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

"""
 Title Graphic Engine
"""
class Title:
    def __init__(self, left, top, width, height, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.font = font

    def display(self, surface, name, ):
        color = TEXT_COLOR
        # Title
        title_surf = self.font.render(name, False, color)
        surface.blit(title_surf, self.rect)



"""
Button Graphic Engine
"""
class Button:
    def __init__(self, text, font, text_color, bg_color):
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color

    def get_width(self):
        return self.font.size(self.text)[0]
    """    
    def get_width(self):
        return self.font.size(self.text)[0]
    """
    def draw(self, surface, x, y, selected):
        button_text = self.font.render(self.text, True, self.text_color if not selected else (255, 0, 0))
        button_rect = button_text.get_rect(center=(x + self.get_width() // 2, y))
        pygame.draw.rect(surface, self.bg_color, button_rect, border_radius=5)
        surface.blit(button_text, button_rect.topleft)
        return button_rect

"""
GameOver Graphic Input Engine
"""
class GameOverInput:
    # Handle Keyboard
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.selected_button = 0
        elif keys[pygame.K_RIGHT]:
            self.selected_button = 1
        elif keys[pygame.K_RETURN]:
            if self.selected_button == 0:
                # Call save function
                pass
            elif self.selected_button == 1:
                # Close the game
                pass
    # Handle TouchScreen
    def handle_touch(self):
        for event in pygame.event.get():
            if event.type == pygame.FINGERDOWN:
                x, y = event.x * self.display_surface.get_width(), event.y * self.display_surface.get_height()
                for i, button in enumerate(self.buttons):
                    if button.rect.collidepoint(x, y):
                        # Lide com o toque no botão (por exemplo, chame a função associada)
                        pass

"""
 GameOver Graphic Engine
"""
class GameOver:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE * 2)
        self.font_buttons = pygame.font.Font(UI_FONT, UI_FONT_SIZE - 4)
        self.title = "Game Over"
        self.player = player
        # button's engine
        self.button_save = Button("Save", self.font_buttons, (255, 255, 255), (100, 100, 100))
        self.button_close = Button("Close", self.font_buttons, (255, 255, 255), (100, 100, 100))
        self.buttons = [self.button_save, self.button_close]
        self.selected_button = 0
        # mouse engine
        self.cursor = MouseCursor()
        self.input = GameOverInput()

    def handle_input(self):
        self.input.handle_input()
    
    def handle_touch(self):
        self.input.handle_touch()

    def display(self):
        self.handle_input()
        # Display title
        title_text = self.font.render(self.title, True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.display_surface.get_width() // 2, 50))
        self.display_surface.blit(title_text, title_rect)

        # Display buttons
        button_spacing = 20
        sum_buttons_width = sum(button.get_width() for button in self.buttons)
        total_buttons = (len(self.buttons) - 1)
        total_width = sum_buttons_width + total_buttons * button_spacing
        x_start = (self.display_surface.get_width() - total_width) // 2
        y = 100
        for i, button in enumerate(self.buttons):
            x = x_start + i * (button.get_width() + button_spacing)
            button_rect = button.draw(self.display_surface, x, y, self.selected_button == i)
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                # Handle mouse hover
                pass
        # Exiba o cursor do mouse
        self.cursor.update()
        self.cursor.draw(self.display_surface)
        # touch engine handle
        self.handle_touch()

