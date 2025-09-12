import pygame
import sys
from helpers import draw_text, draw_points, draw_route, draw_plot, generate_points, PALETTE
from ui_elements import Button, Slider
from ga_classes import Population

pygame.init()
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Otimização de Rotas com Algoritmo Genético")

population_size = 50
mutation_rate = 0.05
num_generations = 1000
num_points = 20

UI_PANEL_HEIGHT = 100
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
BUTTON_Y = 90
BUTTON_RELOAD_X = width - 330
BUTTON_RUN_X = width - 110
BUTTON_REGEN_X = width - 220
SLIDER_WIDTH = 300
SLIDER_HEIGHT = 20
SLIDER_Y_CITIES = 100
SLIDER_Y_GEN = 100
SLIDER_X = 20

button_reload = Button((BUTTON_RELOAD_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), "Recarregar", "reload")
button_regenerate = Button((BUTTON_REGEN_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), "Regerar", "regenerate")
button_run_ga = Button((BUTTON_RUN_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), "Rodar GA", "run")
slider_cities = Slider(SLIDER_X, SLIDER_Y_CITIES, SLIDER_WIDTH, SLIDER_HEIGHT, 2, 200, num_points)
slider_generations = Slider(SLIDER_X + SLIDER_WIDTH + 20, SLIDER_Y_GEN, SLIDER_WIDTH, SLIDER_HEIGHT, 10, 2000, num_generations)

chart_area = pygame.Rect(20, 180, 450, 700)
map_area = pygame.Rect(530, 180, 450, 700)

# Carrega a imagem do mapa e redimensiona para a área de visualização das rotas
try:
    map_background_image = pygame.image.load('map_background.png').convert_alpha()
    map_background_image = pygame.transform.scale(map_background_image, (map_area.width, map_area.height))
except pygame.error as e:
    print(f"Erro ao carregar a imagem do mapa: {e}")
    map_background_image = None

def main():
    global num_points, num_generations, running_ga
    
    points = generate_points(num_points)
    current_population = None
    current_best_individual = None
    generation = 0
    best_fitness_history = []
    
    running = True
    running_ga = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            
            num_points_new = slider_cities.handle_event(event)
            if num_points_new != num_points:
                num_points = num_points_new
                running_ga = False
                points = generate_points(num_points)
                current_population = Population(size=population_size, points=points)
                current_best_individual = current_population.get_fittest()
                generation = 0
                best_fitness_history = []
            
            num_generations_new = slider_generations.handle_event(event)
            if num_generations_new != num_generations:
                num_generations = num_generations_new
                running_ga = False
                generation = 0
                best_fitness_history = []
            
            if button_reload.is_clicked(event):
                running_ga = False
                current_population = Population(size=population_size, points=points)
                current_best_individual = current_population.get_fittest()
                generation = 0
                best_fitness_history = []
            
            if button_run_ga.is_clicked(event):
                if current_population is None:
                    current_population = Population(size=population_size, points=points)
                    current_best_individual = current_population.get_fittest()
                running_ga = not running_ga
                
            
            if button_regenerate.is_clicked(event):
                running_ga = False
                points = generate_points(num_points)
                current_population = Population(size=population_size, points=points)
                current_best_individual = current_population.get_fittest()
                generation = 0
                best_fitness_history = []
                
        if running_ga and generation < num_generations:
            current_population.evolve(mutation_rate, points)
            current_best_individual = current_population.get_fittest()
            best_fitness_history.append(current_best_individual.fitness)
            generation += 1
        
        print_screen(points, current_best_individual, generation, best_fitness_history, current_population)

def get_second_best_individual(population):
    if len(population.population) < 2:
        return None
    best_individual = population.get_fittest()
    temp_population = [ind for ind in population.population if ind != best_individual]
    second_best = max(temp_population, key=lambda x: x.fitness)    
    return second_best

def print_screen(points, current_best_individual, generation, best_fitness_history, current_population):
    screen.fill(PALETTE["background"])

    pygame.draw.rect(screen, PALETTE["secondary"], (0, 70, width, UI_PANEL_HEIGHT))
    draw_text(screen, "Otimização de Rotas - Algoritmo Genético", (width // 2, 40), font_size=48, color=PALETTE["text_dark"])
    button_reload.draw(screen)
    button_regenerate.draw(screen)
    button_run_ga.draw(screen)
    slider_cities.draw(screen)
    slider_generations.draw(screen)
        
    draw_text(screen, f"Cidades: {num_points}", (180, 90), color=PALETTE["text_dark"])
    draw_text(screen, f"Gerações: {generation}/{num_generations}", (490, 90), font_size=20, color=PALETTE["text_dark"])
    
    best_dist = 1/current_best_individual.fitness if current_best_individual and current_best_individual.fitness > 0 else 0
    draw_text(screen, f"Melhor Distância: {best_dist:.2f}", (105, 150), font_size=20, color=PALETTE["text_dark"])

    draw_plot(screen, best_fitness_history, chart_area)
    
    if 'map_background_image' in globals():
        screen.blit(map_background_image, map_area.topleft)
    
    
    if running_ga and current_population:
        second_best_individual = get_second_best_individual(current_population)
        if second_best_individual:
            draw_route(screen, second_best_individual.route, points, (100, 100, 100), thickness=2)
    
    if running_ga and current_best_individual:
        draw_route(screen, current_best_individual.route, points, PALETTE["route_color"], thickness=3)

    draw_points(screen, points)
    
    pygame.display.flip()
    pygame.time.wait(10)

if __name__ == '__main__':
    main()