"""
Elementos de UI para a aplicação de Otimização de Rotas com Algoritmo Genético.

Este módulo define componentes de UI reutilizáveis como botões e sliders para a
interface com Pygame.
"""

import pygame
from helpers import PALETTE

screen = None

class Button:
    """
    Um elemento de UI de botão clicável.

    Atributos:
        rect (pygame.Rect): O retângulo que define a posição e o tamanho do botão.
        text (str): O texto exibido no botão.
        action (str): Um identificador para a ação do botão.
        font (pygame.font.Font): A fonte usada para o texto do botão.
        color (tuple): A cor de fundo do botão.
    """
    def __init__(self, rect, text, action):
        """
        Inicializa um objeto Button.

        Args:
            rect (tuple): Uma tupla (x, y, width, height) para o retângulo do botão.
            text (str): O texto a ser exibido no botão.
            action (str): A ação associada ao botão.
        """
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, 24)
        self.color = PALETTE["secondary"]

    def draw(self, screen):
        """
        Desenha o botão na tela.

        Args:
            screen (pygame.Surface): A tela do Pygame para desenhar.
        """
        shadow_rect = self.rect.copy()
        shadow_rect.move_ip(2, 2)
        pygame.draw.rect(screen, PALETTE["shadow"], shadow_rect, border_radius=10)
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(screen, PALETTE["text_dark"], self.rect, 2, border_radius=10)
        text_surface = self.font.render(self.text, True, PALETTE["text_dark"])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        """
        Verifica se o botão foi clicado.

        Args:
            event (pygame.event.Event): O evento do Pygame a ser verificado.

        Returns:
            bool: True se o botão foi clicado, False caso contrário.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

class Slider:
    """
    Um elemento de UI de slider para selecionar um valor dentro de um intervalo.

    Atributos:
        rect (pygame.Rect): O retângulo para a trilha do slider.
        min_val (int): O valor mínimo do slider.
        max_val (int): O valor máximo do slider.
        val (int): O valor atual do slider.
        handle_pos (int): A coordenada x do manipulador do slider.
        handle_rect (pygame.Rect): O retângulo para o manipulador do slider.
        is_dragging (bool): True se o usuário estiver arrastando o manipulador.
    """
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, is_float=False):
        """
        Inicializa um objeto Slider.

        Args:
            x (int): A coordenada x do slider.
            y (int): A coordenada y do slider.
            w (int): A largura do slider.
            h (int): A altura do slider.
            min_val (int): O valor mínimo.
            max_val (int): O valor máximo.
            initial_val (int): O valor inicial.
            is_float (bool): Se o slider deve usar valores float.
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.is_float = is_float
        self.handle_pos = x + (w * (self.val - min_val) / (max_val - min_val))
        self.handle_rect = pygame.Rect(self.handle_pos - 10, y - 5, 20, h + 10)
        self.is_dragging = False

    def draw(self, screen):
        """
        Desenha o slider na tela.

        Args:
            screen (pygame.Surface): A tela do Pygame para desenhar.
        """
        pygame.draw.rect(screen, PALETTE["shadow"], self.rect, border_radius=5)
        pygame.draw.rect(screen, PALETTE["text_dark"], self.handle_rect, border_radius=5)

    def handle_event(self, event):
        """
        Lida com a interação do usuário com o slider.

        Atualiza o valor do slider com base em eventos do mouse.

        Args:
            event (pygame.event.Event): O evento do Pygame a ser tratado.

        Returns:
            int or float: O valor atual do slider.
        """
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
