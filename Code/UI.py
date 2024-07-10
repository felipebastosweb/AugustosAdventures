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

class WeaponOverlay:
    def __init__(self, display_surface, weapon_graphics, weapon_index, has_switched):
        self.display_surface = display_surface
        self.weapon_graphics = weapon_graphics
        self.weapon_index = weapon_index
        self.has_switched = has_switched

    def show(self):
        bg_rect = SelectionBox(self.display_surface, 10, 630, self.has_switched).show()
        weapon_surf = self.weapon_graphics[self.weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

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
    # TODO: considerar a colocação de JoyPad 
    def handle_event(self, event):
        # TODO: mudar o mecanismo para toque de tela definido em https://www.pygame.org/docs/ref/touch.html
        if event.type == pygame.MOUSEBUTTONDOWN:
            # ... (outros eventos)
            if self.rect.collidepoint(event.pos):
                x_rel, y_rel = event.pos[0] - self.rect.left, event.pos[1] - self.rect.top
                region_x, region_y = x_rel // (self.rect.width // 3), y_rel // (self.rect.height // 3)
                self.joypad_active = True
                self.joypad_direction = (region_x, region_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.joypad_active = False
            self.joypad_direction = None


class UI:
    def __init__(self):
        
        # General
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        
        # Bar Setup
        self.health_bar = Bar(display_surface, font, pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT), HEALTH_COLOR)
        self.energy_bar = Bar(display_surface, font, pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT), ENERGY_COLOR)

        # Selection Boxes
        self.weapon_box = SelectionBox(display_surface, 10, 630, False)
        self.magic_box = SelectionBox(display_surface, 100, 630, False)

        # Exibição da experiência do Player
        self.exp_display = ExperienceDisplay(display_surface, font)

        # Carrega gráficos de armas e magias (substitua com seus dados reais)
        self.weapon_graphics = []  # Carregue os gráficos das armas aqui
        self.magic_graphics = []  # Carregue os gráficos das magias aqui

        """
        # Bar Setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # Convert Weapon Dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon["graphic"]
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        # Convert Magic Dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            magic = pygame.image.load(magic["graphic"]).convert_alpha()
            self.magic_graphics.append(magic)
        """
        
        # JoyPad Setup and State
        self.joypad = JoyPad(JOYPAD_BUTTON_SIZE, JOYPAD_BUTTON_CENTER)
        self.joypad_active = False
        self.joypad_direction = None

    """
    def show_bar(self, current, max_amount, bg_rect, color):
        # Draw Background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # Converting Stats to Pixels
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
    
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
    """

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched) # Weapon Box
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(100, 630, has_switched) # Magix Box (80, 635) in Tutorial
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)
    
    def show_joypad(self):
        self.joypad.draw(self.display_surface)

    def display(self, player):
        # Drawing the Bar
        self.health_bar.show(player.health, player.stats["health"])
        self.energy_bar.show(player.energy, player.stats["energy"])
        """
        self.show_bar(player.health, player.stats["health"], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats["energy"], self.energy_bar_rect, ENERGY_COLOR)
        
        self.show_exp(player.exp)
        """
        self.exp_display.show(player.exp)

        # Mostra as caixas de seleção
        WeaponOverlay(self.display_surface, self.weapon_graphics, player.weapon_index, not player.can_switch_weapon).show()
        MagicOverlay(self.display_surface, self.magic_graphics, player.magic_index, not player.can_switch_magic).show()

        # show joypad in game UI
        self.show_joypad()

        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)