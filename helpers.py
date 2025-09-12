import pygame
import random

PALETTE = {
    "background": (245, 245, 245),
    "primary": (52, 152, 219),
    "secondary": (236, 240, 241),
    "text_dark": (44, 62, 80),
    "text_light": (255, 255, 255),
    "accent": (231, 76, 60),
    "shadow": (200, 200, 200)
}

def generate_points(n):
    """Gera um novo conjunto de n pontos de entrega aleatórios com prioridade e volume."""
    points = []
    for _ in range(n):
        x = random.randint(550, 950)
        y = random.randint(180, 820)
        priority = random.choice([0, 1])
        volume = random.randint(1, 10)
        points.append({'coords': (x, y), 'priority': priority, 'volume': volume})
    return points

def draw_points(screen, points):
    """Desenha os pontos de entrega na tela."""
    for point in points:
        color = PALETTE["accent"] if point['priority'] == 0 else PALETTE["primary"]
        pygame.draw.circle(screen, color, point['coords'], 5)

def draw_route(screen, route, points, color, thickness=2):
    """Desenha uma rota conectando os pontos."""
    if not route:
        return
    for i in range(len(route) - 1):
        pygame.draw.line(screen, color, points[route[i]]['coords'], points[route[i+1]]['coords'], thickness)
    pygame.draw.line(screen, color, points[route[-1]]['coords'], points[route[0]]['coords'], thickness)

def draw_text(screen, text, position, font_size=20, color=PALETTE["text_dark"], center=True):
    """Desenha texto na tela com opções de centralização."""
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    if center:
        text_rect = text_surface.get_rect(center=position)
    else:
        text_rect = text_surface.get_rect(midleft=position)
    screen.blit(text_surface, text_rect)

def draw_graph(screen, history, rect, color, y_label):
    """Desenha um gráfico de linha em uma área específica da tela."""
    if not history or len(history) < 2:
        return

    pygame.draw.rect(screen, PALETTE["secondary"], rect, border_radius=0)
    pygame.draw.rect(screen, PALETTE["text_dark"], rect, 2, border_radius=0)
    
    min_val = min(history) if history else 0
    max_val = max(history) if history else 1
    
    if max_val == min_val:
        max_val += 0.01

    points_to_draw = []
    for i, val in enumerate(history):
        x_norm = i / (len(history) - 1)
        x_pos = rect.x + x_norm * rect.width
        
        y_norm = (val - min_val) / (max_val - min_val)
        y_pos = rect.y + y_norm * rect.height
        
        points_to_draw.append((x_pos, y_pos))

    pygame.draw.lines(screen, color, False, points_to_draw, 3)
    
    draw_text(screen, y_label, (rect.x + rect.width / 2, rect.y + 15), font_size=24)
    
    if points_to_draw:
        draw_text(screen, f"{history[-1]:.4f}", (points_to_draw[-1][0] + 30, points_to_draw[-1][1]), font_size=18, color=PALETTE["text_dark"], center=False)