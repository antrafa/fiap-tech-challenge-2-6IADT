"""Ponto de entrada e loop principal da aplicação de otimização de rotas."""

import pygame
import sys
from helpers import draw_text, draw_points, draw_route, draw_plot, draw_legend, generate_points, generate_llm_report, PALETTE
from ui_elements import Button, Slider
from ga_classes import Population

pygame.init()
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Otimização de Rotas com Algoritmo Genético")

# --- Constantes e Configuração de Layout ---
UI_PANEL_Y = 70
UI_PANEL_HEIGHT = 180
CHART_MAP_Y = UI_PANEL_Y + UI_PANEL_HEIGHT + 20
CHART_MAP_HEIGHT = height - CHART_MAP_Y - 20

BUTTON_MARGIN = 15
BUTTON_WIDTH = (width / 4) - 21
BUTTON_HEIGHT = 40
BUTTON_Y = UI_PANEL_Y + 120
BUTTON_RELOAD_X = BUTTON_MARGIN
BUTTON_REGEN_X = BUTTON_RELOAD_X + BUTTON_WIDTH + BUTTON_MARGIN
BUTTON_RUN_X = BUTTON_REGEN_X + BUTTON_WIDTH + BUTTON_MARGIN
BUTTON_REPORT_X = BUTTON_RUN_X + BUTTON_WIDTH + BUTTON_MARGIN

SLIDER_WIDTH = 320
SLIDER_HEIGHT = 15
SLIDER_X_COL1 = 20
SLIDER_X_COL2 = 380
SLIDER_X_COL3 = 500
SLIDER_X_COL4 = 740
SLIDER_Y_ROW1 = UI_PANEL_Y + 20
SLIDER_Y_ROW2 = UI_PANEL_Y + 70

# --- Inicialização dos Parâmetros ---
initial_num_points = 20
initial_num_generations = 1000
initial_population_size = 50
initial_mutation_rate = 0.05

# --- Inicialização dos Elementos de UI ---
button_reload = Button((BUTTON_RELOAD_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), "Reiniciar", "reload")
button_regenerate = Button((BUTTON_REGEN_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), "Gerar cidades", "regenerate")
button_run_ga = Button((BUTTON_RUN_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), "Rodar GA", "run")
button_generate_report = Button((BUTTON_REPORT_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), "Gerar Relatório", "report")

slider_cities = Slider(SLIDER_X_COL1, SLIDER_Y_ROW1, SLIDER_WIDTH, SLIDER_HEIGHT, 2, 200, initial_num_points)
slider_generations = Slider(SLIDER_X_COL2, SLIDER_Y_ROW1, SLIDER_WIDTH, SLIDER_HEIGHT, 10, 2000, initial_num_generations)
slider_population = Slider(SLIDER_X_COL1, SLIDER_Y_ROW2, SLIDER_WIDTH, SLIDER_HEIGHT, 10, 200, initial_population_size)
slider_mutation = Slider(SLIDER_X_COL2, SLIDER_Y_ROW2, SLIDER_WIDTH, SLIDER_HEIGHT, 0.01, 0.5, initial_mutation_rate, is_float=True)

chart_area = pygame.Rect(20, CHART_MAP_Y, 450, CHART_MAP_HEIGHT)
map_area = pygame.Rect(530, CHART_MAP_Y, 450, CHART_MAP_HEIGHT)

# Carrega e redimensiona a imagem de fundo do mapa
try:
    map_background_image = pygame.image.load('map_background.png').convert_alpha()
    map_background_image = pygame.transform.scale(map_background_image, (map_area.width, map_area.height))
except pygame.error as e:
    print(f"Erro ao carregar a imagem do mapa: {e}")
    map_background_image = None


def main():
    """Função principal que executa o loop da aplicação, lida com eventos e atualiza a tela."""
    # Variáveis de estado da simulação
    num_points = initial_num_points
    num_generations = initial_num_generations
    population_size = initial_population_size
    mutation_rate = initial_mutation_rate
    
    points = generate_points(num_points)
    
    # Inicializa a população
    current_population = Population(size=int(population_size), points=points)
    current_best_individual = current_population.get_fittest()
    generation = 0
    best_fitness_history = []
    
    running = True
    running_ga = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            
            # --- Lida com eventos da UI ---
            
            # Sliders
            new_num_points = slider_cities.handle_event(event)
            if new_num_points != num_points:
                num_points = new_num_points
                points = generate_points(num_points)
                running_ga = False
                current_population = Population(size=int(population_size), points=points)
                current_best_individual = current_population.get_fittest()
                generation = 0
                best_fitness_history = []

            new_num_generations = slider_generations.handle_event(event)
            if new_num_generations != num_generations:
                num_generations = new_num_generations
                
            new_population_size = slider_population.handle_event(event)
            if new_population_size != population_size:
                population_size = new_population_size
                running_ga = False
                current_population = Population(size=int(population_size), points=points)
                current_best_individual = current_population.get_fittest()
                generation = 0
                best_fitness_history = []

            new_mutation_rate = slider_mutation.handle_event(event)
            if new_mutation_rate != mutation_rate:
                mutation_rate = new_mutation_rate
            
            # Botões
            if button_reload.is_clicked(event):
                running_ga = False
                current_population = Population(size=int(population_size), points=points)
                current_best_individual = current_population.get_fittest()
                generation = 0
                best_fitness_history = []
            
            if button_run_ga.is_clicked(event):
                running_ga = not running_ga
                
            if button_regenerate.is_clicked(event):
                running_ga = False
                points = generate_points(num_points)
                current_population = Population(size=int(population_size), points=points)
                current_best_individual = current_population.get_fittest()
                generation = 0
                best_fitness_history = []
            
            if button_generate_report.is_clicked(event):
                # A classe do botão já impede o clique se estiver desabilitado
                generate_llm_report(screen, width, height, current_best_individual, points)

        # --- Lógica de Evolução do AG ---
        if running_ga and generation < num_generations:
            current_population.evolve(mutation_rate, points)
            current_best_individual = current_population.get_fittest()
            best_fitness_history.append(current_best_individual.fitness)
            generation += 1
        
        # --- Atualiza a Tela ---
        print_screen(
            screen, points, current_best_individual, generation, num_generations, 
            best_fitness_history, current_population, running_ga, num_points, 
            population_size, mutation_rate
        )

def get_second_best_individual(population):
    """Encontra o segundo indivíduo mais apto da população."""
    if not population or len(population.population) < 2:
        return None
    best_individual = population.get_fittest()
    temp_population = [ind for ind in population.population if ind != best_individual]
    if not temp_population:
        return None
    second_best = max(temp_population, key=lambda x: x.fitness)    
    return second_best

def print_screen(screen, points, current_best_individual, generation, num_generations, best_fitness_history, current_population, running_ga, num_points, population_size, mutation_rate):
    """Lida com todas as operações de desenho na tela."""
    screen.fill(PALETTE["background"])

    # Desenha o painel da UI e os elementos
    pygame.draw.rect(screen, PALETTE["secondary"], (0, UI_PANEL_Y, width, UI_PANEL_HEIGHT))
    draw_text(screen, "Otimização de Rotas - Algoritmo Genético", (width // 2, 40), font_size=48, color=PALETTE["text_dark"])
    
    # --- Lógica dos Botões ---
    # Habilita/desabilita o botão de relatório
    button_generate_report.disabled = (generation < num_generations)
    # Alterna o texto do botão de execução
    button_run_ga.text = "Pausar" if running_ga else "Rodar GA"
    
    # Desenha os botões
    button_reload.draw(screen)
    button_regenerate.draw(screen)
    button_run_ga.draw(screen)
    button_generate_report.draw(screen)
    
    # Desenha sliders e seus valores
    slider_cities.draw(screen)
    draw_text(screen, f"Cidades: {int(num_points)}", (SLIDER_X_COL1 + SLIDER_WIDTH / 2, SLIDER_Y_ROW1 + 25), color=PALETTE["text_dark"])
    
    slider_generations.draw(screen)
    draw_text(screen, f"Gerações: {int(num_generations)}", (SLIDER_X_COL2 + SLIDER_WIDTH / 2, SLIDER_Y_ROW1 + 25), color=PALETTE["text_dark"])

    slider_population.draw(screen)
    draw_text(screen, f"População: {int(population_size)}", (SLIDER_X_COL1 + SLIDER_WIDTH / 2, SLIDER_Y_ROW2 + 25), color=PALETTE["text_dark"])

    slider_mutation.draw(screen)
    draw_text(screen, f"Mutação: {mutation_rate:.2f}", (SLIDER_X_COL2 + SLIDER_WIDTH / 2, SLIDER_Y_ROW2 + 25), color=PALETTE["text_dark"])

    # Desenha informações de status
    draw_text(screen, f"Geração Atual: {generation}", (SLIDER_X_COL3 + 350, SLIDER_Y_ROW1), font_size=20, color=PALETTE["text_dark"])
    
    best_dist = 1/current_best_individual.fitness if current_best_individual and current_best_individual.fitness > 0 else 0
    draw_text(screen, f"Melhor Distância: {best_dist:.2f}", (SLIDER_X_COL3 + 350, SLIDER_Y_ROW1 + 30), font_size=20, color=PALETTE["text_dark"])

    if current_population:
        avg_fitness = current_population.get_average_fitness()
        avg_dist = 1/avg_fitness if avg_fitness > 0 else 0
        draw_text(screen, f"Distância Média: {avg_dist:.2f}", (SLIDER_X_COL3 + 350, SLIDER_Y_ROW1 + 60), font_size=20, color=PALETTE["text_dark"])

    # Desenha o gráfico de aptidão
    draw_plot(screen, best_fitness_history, chart_area)
    
    # Desenha o fundo do mapa
    if 'map_background_image' in globals() and map_background_image:
        screen.blit(map_background_image, map_area.topleft)
    
    # Desenha a legenda dos pontos
    draw_legend(screen, (map_area.left + 10, map_area.bottom - 70))

    # Desenha as rotas apenas se a simulação tiver começado
    if generation > 0:
        if current_population:
            second_best_individual = get_second_best_individual(current_population)
            if second_best_individual:
                draw_route(screen, second_best_individual.route, points, (100, 100, 100), thickness=2)
        
        if current_best_individual:
            draw_route(screen, current_best_individual.route, points, PALETTE["route_color"], thickness=3)

    # Desenha os pontos
    draw_points(screen, points)
    
    pygame.display.flip()
    pygame.time.wait(10)

if __name__ == '__main__':
    main()