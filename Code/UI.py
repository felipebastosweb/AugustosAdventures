import pygame
from Settings import *
import os

# This is for file (images specifically) importing (This line changes the directory to where the project is saved)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Bar:
    def __init__(self, display_surface, font, bg_rect, color):
        self.display_surface = display_surface
        self.font = font
        self.bg_rect = bg_rect
        self.color = color

    def show(self, current, max_amount):
        # Draw Background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.bg_rect)

        # Converting Stats to Pixels
        ratio = current / max_amount
        current_width = self.bg_rect.width * ratio
        current_rect = self.bg_rect.copy()
        current_rect.width = current_width

        # Drawing the Bar
        pygame.draw.rect(self.display_surface, self.color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.bg_rect, 3)

class SelectionBox:
    def __init__(self, display_surface, left, top, has_switched):
        self.display_surface = display_surface
        self.bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        self.has_switched = has_switched

    def show(self):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.bg_rect)
        if self.has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, self.bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.bg_rect, 3)
        return self.bg_rect

class GraphicOverlay:
    def __init__(self, position, display_surface, data, index, has_switched):
        self.position = position
        self.display_surface = display_surface
        self.graphics = []
        self.init_graphics(data)
        self.index = index
        self.has_switched = has_switched
    # init list of images
    def init_graphics(self, data):
        for item in data.values():
            path = item["graphic"]
            item = pygame.image.load(path).convert_alpha()
            self.graphics.append(item)
    def update(self, index, has_switched):
        self.index = index
        self.has_switched = has_switched
    def show(self):
        bg_rect = SelectionBox(self.display_surface, self.position[0], self.position[1], self.has_switched).show()
        surface = self.graphics[self.index]
        rect = surface.get_rect(center=bg_rect.center)
        self.display_surface.blit(surface, rect)

class ExperienceDisplay:
    def __init__(self, display_surface, font):
        self.display_surface = display_surface
        self.font = font

    def show(self, exp):
        texto_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        retangulo_texto = texto_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, retangulo_texto.inflate(20, 20))
        self.display_surface.blit(texto_surf, retangulo_texto)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, retangulo_texto.inflate(20, 20), 3)

# TODO: mudar o mecanismo para toque de tela definido em https://www.pygame.org/docs/ref/touch.html e https://www.makeuseof.com/pygame-touch-inputs-working-with/
""" Prototipando um JoyPad para adaptar o jogo ao dispositivo mobile """
class JoyPad:
    def __init__(self, size, center):
        self.rect = pygame.Rect(10, 600, size, size)
        self.rect.center = center
        self.active_region = None

    def draw(self, surface):
        pygame.draw.rect(surface, JOYPAD_COLOR_GRAY, self.rect)
        if self.active_region:
            x, y = self.active_region
            pygame.draw.circle(surface, JOYPAD_COLOR_WHITE, (self.rect.left + x * (self.rect.width // 3), self.rect.top + y * (self.rect.height // 3)), 10)

    def handle_event(self, event):
        if event.type == pygame.FINGERDOWN:
            touch_x, touch_y = event.x * self.rect.width, event.y * self.rect.height
            x_rel, y_rel = touch_x - self.rect.left, touch_y - self.rect.top
            region_x, region_y = x_rel // (self.rect.width // 3), y_rel // (self.rect.height // 3)
            self.active_region = (region_x, region_y)
        elif event.type == pygame.FINGERUP:
            self.active_region = None


class UI:
    def __init__(self):
        
        # General
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        
        # Bar Setup
        self.health_bar = Bar(self.display_surface, self.font, pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT), HEALTH_COLOR)
        self.energy_bar = Bar(self.display_surface, self.font, pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT), ENERGY_COLOR)

        # Selection Boxes
        self.weapon_box = SelectionBox(self.display_surface, 10, 630, False)
        self.magic_box = SelectionBox(self.display_surface, 100, 630, False)

        # Exibição da experiência do Player
        self.exp_display = ExperienceDisplay(self.display_surface, self.font)

        # Carrega gráficos de armas e magias (substitua com seus dados reais)
        self.weapon_overlay = GraphicOverlay((10, 630), self.display_surface, weapon_data, 0, False)
        self.magic_overlay = GraphicOverlay((100, 630), self.display_surface, magic_data, 0, False)
        #self.weapon_overlay = WeaponOverlay(self.display_surface, weapon_data, 0, False)
        #self.magic_overlay = MagicOverlay(self.display_surface, magic_data, 0, False)
        
        # JoyPad Setup and State
        self.joypad = JoyPad(JOYPAD_BUTTON_SIZE, JOYPAD_BUTTON_CENTER)
        self.joypad_active = False
        self.joypad_direction = None

    def show_joypad(self):
        self.joypad.draw(self.display_surface)

    def display(self, player):
        # Drawing the Bar
        self.health_bar.show(player.health, player.stats["health"])
        self.energy_bar.show(player.energy, player.stats["energy"])
        self.exp_display.show(player.exp)

        # Mostra as caixas de seleção
        self.weapon_overlay.update(player.weapon_index, player.can_switch_weapon)
        self.weapon_overlay.show()
        self.magic_overlay.update(player.magic_index, player.can_switch_magic)
        self.magic_overlay.show()

        # show joypad in game UI
        self.show_joypad()
