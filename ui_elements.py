"""Define componentes de UI reutilizáveis (botões, sliders) para Pygame."""

import pygame
from helpers import PALETTE

screen = None

class Button:
    """Um elemento de UI de botão clicável com estado de desabilitado."""
    def __init__(self, rect, text, action):
        """Inicializa um botão com posição, texto e ação."""
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, 24)
        self.color = PALETTE["secondary"]
        self.disabled_color = (200, 200, 200)
        self.disabled = False

    def draw(self, screen):
        """Desenha o botão na tela, com aparência de desabilitado se necessário."""
        bg_color = self.disabled_color if self.disabled else self.color
        text_color = (100, 100, 100) if self.disabled else PALETTE["text_dark"]
        border_color = (150, 150, 150) if self.disabled else PALETTE["text_dark"]

        shadow_rect = self.rect.copy()
        shadow_rect.move_ip(2, 2)
        pygame.draw.rect(screen, PALETTE["shadow"], shadow_rect, border_radius=10)
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=10)
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        """Verifica se o botão foi clicado, retornando False se estiver desabilitado."""
        if self.disabled:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

class Slider:
    """Um elemento de UI de slider para selecionar um valor numérico."""
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, is_float=False):
        """Inicializa um slider com um intervalo de valores e valor inicial."""
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.is_float = is_float
        self.handle_pos = x + (w * (self.val - min_val) / (max_val - min_val))
        self.handle_rect = pygame.Rect(self.handle_pos - 10, y - 5, 20, h + 10)
        self.is_dragging = False

    def draw(self, screen):
        """Desenha o slider na tela."""
        pygame.draw.rect(screen, PALETTE["shadow"], self.rect, border_radius=5)
        pygame.draw.rect(screen, PALETTE["text_dark"], self.handle_rect, border_radius=5)

    def handle_event(self, event):
        """Lida com a interação do mouse para arrastar o slider e atualizar seu valor."""
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
            
            if not self.is_float:
                self.val = int(round(self.val))
            
            self.handle_rect.centerx = self.handle_pos
        return self.val
