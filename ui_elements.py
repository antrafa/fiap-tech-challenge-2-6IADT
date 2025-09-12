import pygame
import sys

PALETTE = {
    "background": (245, 245, 245),
    "primary": (52, 152, 219),
    "secondary": (236, 240, 241),
    "text_dark": (44, 62, 80),
    "text_light": (255, 255, 255),
    "accent": (231, 76, 60),
    "shadow": (200, 200, 200)
}
screen = None

class Button:
    def __init__(self, rect, text, action, screen_instance):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, 24)
        self.color = PALETTE["secondary"]
        self.screen = screen_instance

    def draw(self):
        shadow_rect = self.rect.copy()
        shadow_rect.move_ip(2, 2)
        pygame.draw.rect(self.screen, PALETTE["shadow"], shadow_rect, border_radius=10)
        
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(self.screen, PALETTE["text_dark"], self.rect, 2, border_radius=10)
        text_surface = self.font.render(self.text, True, PALETTE["text_dark"])
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, screen_instance):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.handle_pos = x + (w * (self.val - min_val) / (max_val - min_val))
        self.handle_rect = pygame.Rect(self.handle_pos - 10, y - 5, 20, h + 10)
        self.is_dragging = False
        self.screen = screen_instance

    def draw(self):
        pygame.draw.rect(self.screen, PALETTE["shadow"], self.rect, border_radius=5)
        pygame.draw.rect(self.screen, PALETTE["text_dark"], self.handle_rect, border_radius=5)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.handle_rect.collidepoint(event.pos):
            self.is_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.handle_pos = event.pos[0]
            if self.handle_pos < self.rect.x:
                self.handle_pos = self.rect.x
            elif self.handle_pos > self.rect.x + self.rect.width:
                self.handle_pos = self.rect.x + self.rect.width
            
            self.val = self.min_val + (self.handle_pos - self.rect.x) / self.rect.width * (self.max_val - self.min_val)
            self.val = int(round(self.val))
            self.handle_rect.centerx = self.handle_pos
        return self.val