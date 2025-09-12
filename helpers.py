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
    "point_critical": (0, 0, 139),
    "point_regular": (0, 100, 0),
    "point_glow": (255, 255, 0),
}

# PALETTE = {
#     "background": (255, 248, 220),
#     "primary": (139, 69, 19),
#     "secondary": (222, 184, 135),
#     "text_dark": (70, 40, 20),
#     "text_light": (255, 255, 255),
#     "accent": (165, 42, 42),
#     "shadow": (184, 134, 11)          # Tom de ouro velho para sombras
# }

def generate_points(n):
    points = []
    for _ in range(n):
        x = random.randint(550, 950)
        y = random.randint(180, 820)
        priority = random.choice([0, 1])
        volume = random.randint(1, 10)
        points.append({'coords': (x, y), 'priority': priority, 'volume': volume})
    return points

def draw_points(screen, points):
    for point in points:
        color = PALETTE["point_critical"] if point['priority'] == 0 else PALETTE["point_regular"]
        pygame.draw.circle(screen, color, point['coords'], 5)

def draw_route(screen, route, points, color, thickness=2):
    if not route:
        return
    for i in range(len(route) - 1):
        pygame.draw.line(screen, color, points[route[i]]['coords'], points[route[i+1]]['coords'], thickness)
    pygame.draw.line(screen, color, points[route[-1]]['coords'], points[route[0]]['coords'], thickness)

def draw_text(screen, text, position, font_size=20, color=PALETTE["text_dark"], center=True):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    if center:
        text_rect = text_surface.get_rect(center=position)
    else:
        text_rect = text_surface.get_rect(midleft=position)
    screen.blit(text_surface, text_rect)

def convert_color(rgb_tuple):
    return (rgb_tuple[0] / 255.0, rgb_tuple[1] / 255.0, rgb_tuple[2] / 255.0)

def draw_plot(screen, history, rect, x_label='Geração', y_label='Aptidão'):
    if not history:
        return
    generations = list(range(len(history)))
    line_color = convert_color(PALETTE['primary'])
    fig, ax = plt.subplots(figsize=(rect.width / 100, rect.height / 100), dpi=100)
    ax.plot(generations, history, color=line_color)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title("Evolução da Aptidão")
    ax.grid(True)
    plt.tight_layout()
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_argb()
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "ARGB")
    plt.close(fig)
    screen.blit(surf, rect.topleft)