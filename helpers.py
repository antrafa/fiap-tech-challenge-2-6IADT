"""Funções auxiliares para desenho, geração de dados e chamadas de API."""

import os
import random
import pygame
import openai
from dotenv import load_dotenv
from ga_classes import Individual
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

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
    """Gera uma lista de `n` pontos aleatórios com coordenadas, prioridade e volume."""
    points = []
    for _ in range(n):
        x = random.randint(550, 950)
        y = random.randint(280, 880)
        priority = random.choice([0, 1])
        volume = random.randint(1, 10)
        points.append({'coords': (x, y), 'priority': priority, 'volume': volume})
    return points

def draw_points(screen, points):
    """Desenha os pontos de entrega na tela."""
    for point in points:
        color = PALETTE["point_critical"] if point['priority'] == 1 else PALETTE["point_regular"]
        pygame.draw.circle(screen, color, point['coords'], 5)

def draw_legend(screen, position):
    """Desenha a legenda de cores dos pontos na tela."""
    font = pygame.font.Font(None, 22)
    background_color = (255, 255, 255, 180)
    legend_items = [
        (PALETTE["point_critical"], "Ponto Prioritário (Urgente)"),
        (PALETTE["point_regular"], "Ponto Regular")
    ]
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
    """Desenha uma rota (lista de pontos) na tela."""
    if not route:
        return
    for i in range(len(route) - 1):
        pygame.draw.line(screen, color, points[route[i]]['coords'], points[route[i+1]]['coords'], thickness)
    pygame.draw.line(screen, color, points[route[-1]]['coords'], points[route[0]]['coords'], thickness)

def draw_text(screen, text, position, font_size=20, color=PALETTE["text_dark"], center=True):
    """Renderiza e exibe um texto na tela."""
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    if center:
        text_rect = text_surface.get_rect(center=position)
    else:
        text_rect = text_surface.get_rect(midleft=position)
    screen.blit(text_surface, text_rect)

def convert_color(rgb_tuple):
    """Converte uma cor RGB para o formato do Matplotlib (0-1)."""
    return (rgb_tuple[0] / 255.0, rgb_tuple[1] / 255.0, rgb_tuple[2] / 255.0)

def draw_plot(screen, history, rect, x_label='Geração', y_label='Aptidão'):
    """Desenha o gráfico de evolução da aptidão usando Matplotlib."""
    if not history:
        placeholder_color = (220, 220, 220)
        pygame.draw.rect(screen, placeholder_color, rect, border_radius=10)
        draw_text(screen, "Aguardando simulação...", rect.center, font_size=20, color=(100, 100, 100))
        return

    generations = list(range(len(history)))
    line_color = convert_color(PALETTE['primary'])
    fig, ax = plt.subplots(figsize=(rect.width / 100, rect.height / 100), dpi=100)
    ax.plot(generations, history, color=line_color)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title("Evolução da Aptidão")
    ax.grid(True)
    plt.tight_layout(pad=0.5)
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_argb()
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "ARGB")
    plt.close(fig)
    scaled_surf = pygame.transform.scale(surf, (rect.width, rect.height))
    screen.blit(scaled_surf, rect.topleft)

def generate_llm_report(screen, width, height, best_individual, points):
    """Gera um relatório de rota em Markdown usando a API da OpenAI, mostrando uma tela de loading."""
    # --- Tela de Loading ---
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Overlay preto semi-transparente
    screen.blit(overlay, (0, 0))
    draw_text(screen, "Gerando relatório com IA...", (width // 2, height // 2 - 20), font_size=30, color=PALETTE["text_light"])
    draw_text(screen, "Aguarde, a tela pode congelar por alguns segundos.", (width // 2, height // 2 + 20), font_size=20, color=PALETTE["text_light"])
    pygame.display.flip()

    print("Gerando relatório com a API da OpenAI... Isso pode levar alguns segundos.")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "SUA_CHAVE_DA_API_AQUI":
        print("ERRO: Chave da API da OpenAI não configurada.")
        print("Por favor, defina a variável de ambiente OPENAI_API_KEY no arquivo .env")
        return

    client = openai.OpenAI(api_key=api_key)

    # --- 1. Coleta e Formatação dos Dados ---
    route_indices = best_individual.route
    ordered_points = [points[i] for i in route_indices]
    total_distance = 1 / best_individual.fitness if best_individual.fitness > 0 else float('inf')
    total_volume = sum(p['volume'] for p in ordered_points)

    # Calcula a distância de uma rota não otimizada (sequencial) para comparação
    naive_route = list(range(len(points)))
    naive_dist = 0
    for i in range(len(naive_route) - 1):
        naive_dist += Individual.get_distance(points[naive_route[i]]['coords'], points[naive_route[i+1]]['coords'])
    naive_dist += Individual.get_distance(points[naive_route[-1]]['coords'], points[naive_route[0]]['coords'])

    # --- 2. Criação do Prompt Único e Eficiente ---
    prompt = f"""Você é um assistente de logística. Sua tarefa é gerar um relatório completo sobre uma rota de entrega otimizada por um algoritmo genético. O relatório deve ser em formato Markdown e conter exatamente as seguintes seções:

1.  **Instruções para o Motorista:** Um guia passo a passo claro e direto.
2.  **Relatório de Eficiência:** Uma análise comparando a rota otimizada com uma rota não otimizada, incluindo a porcentagem de economia.
3.  **Sugestões de Melhoria:** Com base nos dados da rota, sugira melhorias no processo logístico.
4.  **Perguntas e Respostas:** Responda a um conjunto de perguntas comuns sobre a rota.

**Dados da Rota para Análise:**
- **Rota Otimizada (sequência de índices):** {route_indices}
- **Pontos (com coordenadas, prioridade e volume):** {[(p['coords'], p['priority'], p['volume']) for p in ordered_points]}
- **Distância Total da Rota Otimizada:** {total_distance:.2f} km
- **Distância de uma Rota Não Otimizada (para comparação):** {naive_dist:.2f} km
- **Volume Total da Carga:** {total_volume}
- **Capacidade Máxima do Veículo:** 50

Por favor, gere o relatório completo com base nestes dados."""

    # --- 3. Chamada à API da OpenAI (BLOQUEANTE) ---
    try:
        print("Fazendo chamada à API... A interface irá congelar.")
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente de logística que gera relatórios em Markdown."},
                {"role": "user", "content": prompt}
            ]
        )
        llm_response = completion.choices[0].message.content
        print("Resposta da API recebida.")

        # --- 4. Salvando o Relatório ---
        final_report = f"# Relatório de Rota Otimizada (Gerado por IA)\n\n" + llm_response
        with open("RELATORIO_DE_ROTA.md", "w", encoding="utf-8") as f:
            f.write(final_report)
        print("Relatório salvo com sucesso em RELATORIO_DE_ROTA.md")

    except Exception as e:
        print(f"Ocorreu um erro ao chamar a API da OpenAI: {e}")