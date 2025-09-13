"""
Funções auxiliares para a aplicação de Otimização de Rotas com Algoritmo Genético.

Este módulo fornece funções para gerar dados, desenhar elementos de UI na tela
do Pygame e outras funções utilitárias.
"""

import random
import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

PALETTE = {
    "background": (245, 245, 245),
    "primary": (52, 152, 219),
    "secondary": (236, 240, 241),
    "text_dark": (44, 62, 80),
    "text_light": (255, 255, 255),
    "accent": (231, 76, 60),
    "shadow": (200, 200, 200),
    "route_color": (173, 216, 230),
    "route_minor_color": (190, 160, 130),
    "point_critical": (231, 76, 60),
    "point_regular": (0, 0, 139),
    "point_glow": (255, 255, 0),
}

def generate_points(n):
    """
    Gera uma lista de pontos aleatórios.

    Cada ponto é um dicionário contendo suas coordenadas, um nível de prioridade
    e um volume.

    Args:
        n (int): O número de pontos a serem gerados.

    Returns:
        list: Uma lista de dicionários de pontos.
    """
    points = []
    for _ in range(n):
        x = random.randint(550, 950)
        y = random.randint(280, 880)
        priority = random.choice([0, 1])
        volume = random.randint(1, 10)
        points.append({'coords': (x, y), 'priority': priority, 'volume': volume})
    return points

def draw_points(screen, points):
    """
    Desenha os pontos de entrega na tela.

    Args:
        screen (pygame.Surface): A tela do Pygame para desenhar.
        points (list): Uma lista de dicionários de pontos.
    """
    for point in points:
        # Corrigido: Pontos com prioridade 1 são os críticos (urgentes)
        color = PALETTE["point_critical"] if point['priority'] == 1 else PALETTE["point_regular"]
        pygame.draw.circle(screen, color, point['coords'], 5)

def draw_legend(screen, position):
    """
    Desenha a legenda de cores dos pontos na tela.

    Args:
        screen (pygame.Surface): A tela para desenhar.
        position (tuple): A coordenada (x, y) do canto superior esquerdo da legenda.
    """
    font = pygame.font.Font(None, 22)
    background_color = (255, 255, 255, 180)  # Branco com transparência
    
    # Itens da legenda
    legend_items = [
        (PALETTE["point_critical"], "Ponto Prioritário (Urgente)"),
        (PALETTE["point_regular"], "Ponto Regular")
    ]
    
    # Cria uma superfície para a legenda para lidar com a transparência
    legend_surface = pygame.Surface((250, 60), pygame.SRCALPHA)
    pygame.draw.rect(legend_surface, background_color, legend_surface.get_rect(), border_radius=10)
    
    y_offset = 15
    for color, text in legend_items:
        pygame.draw.circle(legend_surface, color, (20, y_offset), 5)
        text_surface = font.render(text, True, PALETTE["text_dark"])
        legend_surface.blit(text_surface, (35, y_offset - 8))
        y_offset += 25
        
    screen.blit(legend_surface, position)

def draw_route(screen, route, points, color, thickness=2):
    """
    Desenha uma rota na tela.

    Args:
        screen (pygame.Surface): A tela do Pygame para desenhar.
        route (list): Uma lista de índices de pontos representando a rota.
        points (list): Uma lista de todos os dicionários de pontos.
        color (tuple): A cor da rota.
        thickness (int): A espessura das linhas da rota.
    """
    if not route:
        return
    for i in range(len(route) - 1):
        pygame.draw.line(screen, color, points[route[i]]['coords'], points[route[i+1]]['coords'], thickness)
    pygame.draw.line(screen, color, points[route[-1]]['coords'], points[route[0]]['coords'], thickness)

def draw_text(screen, text, position, font_size=20, color=PALETTE["text_dark"], center=True):
    """
    Renderiza e exibe texto na tela.

    Args:
        screen (pygame.Surface): A tela do Pygame para desenhar.
        text (str): O texto a ser exibido.
        position (tuple): As coordenadas (x, y) para o texto.
        font_size (int): O tamanho da fonte.
        color (tuple): A cor do texto.
        center (bool): Se deve centralizar o texto na posição fornecida.
    """
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    if center:
        text_rect = text_surface.get_rect(center=position)
    else:
        text_rect = text_surface.get_rect(midleft=position)
    screen.blit(text_surface, text_rect)

def convert_color(rgb_tuple):
    """
    Converte uma tupla de cor RGB para um formato adequado para o Matplotlib (escala 0-1).

    Args:
        rgb_tuple (tuple): Uma tupla de cor RGB (ex: (255, 0, 0)).

    Returns:
        tuple: Uma tupla de cor com valores dimensionados entre 0 e 1.
    """
    return (rgb_tuple[0] / 255.0, rgb_tuple[1] / 255.0, rgb_tuple[2] / 255.0)

def draw_plot(screen, history, rect, x_label='Geração', y_label='Aptidão'):
    """
    Desenha o gráfico de evolução da aptidão na tela.

    Usa o Matplotlib para gerar o gráfico e depois o desenha na tela do Pygame.

    Args:
        screen (pygame.Surface): A tela do Pygame para desenhar.
        history (list): Uma lista de valores de aptidão ao longo das gerações.
        rect (pygame.Rect): A área retangular para desenhar o gráfico.
        x_label (str): O rótulo para o eixo x.
        y_label (str): O rótulo para o eixo y.
    """
    # Desenha um placeholder se não houver histórico
    if not history:
        placeholder_color = (220, 220, 220)
        pygame.draw.rect(screen, placeholder_color, rect, border_radius=10)
        draw_text(screen, "Aguardando simulação...", rect.center, font_size=20, color=(100, 100, 100))
        return

    generations = list(range(len(history)))
    line_color = convert_color(PALETTE['primary'])
    
    # Cria a figura do Matplotlib com o tamanho correto
    fig, ax = plt.subplots(figsize=(rect.width / 100, rect.height / 100), dpi=100)
    ax.plot(generations, history, color=line_color)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title("Evolução da Aptidão")
    ax.grid(True)
    plt.tight_layout(pad=0.5)
    
    # Renderiza o canvas do Matplotlib
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_argb()
    size = canvas.get_width_height()
    
    # Converte para uma superfície do Pygame
    surf = pygame.image.fromstring(raw_data, size, "ARGB")
    plt.close(fig)
    
    # Redimensiona a superfície para caber exatamente no retângulo e a desenha
    scaled_surf = pygame.transform.scale(surf, (rect.width, rect.height))
    screen.blit(scaled_surf, rect.topleft)