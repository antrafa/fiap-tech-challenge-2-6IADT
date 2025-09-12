import pygame
import sys
from ga_manager import GeneticAlgorithmManager
from ui_elements import Button, Slider
from helpers import draw_text, draw_points, draw_route, draw_graph, PALETTE

pygame.init()
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Otimização de Rotas com Algoritmo Genético")

population_size = 50
mutation_rate = 0.05
num_generations = 1000
num_points = 20

UI_PANEL_HEIGHT = 80

title_text = "Otimização de Rotas - Algoritmo Genético"
button_reload = Button((width - 320, 90, 150, 40), "Recarregar", "reload", screen)
button_run_ga = Button((width - 160, 90, 150, 40), "Rodar GA", "run", screen)
slider_cities = Slider(20, 100, 300, 20, 2, 200, num_points, screen)
slider_generations = Slider(340, 100, 300, 20, 10, 2000, num_generations, screen)

chart_area = pygame.Rect(20, 180, 450, 700)
map_area = pygame.Rect(530, 180, 450, 700)

def main():
    ga_manager = GeneticAlgorithmManager(num_points, population_size, mutation_rate, num_generations)
    
    running_ga = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            
            num_points_new = slider_cities.handle_event(event)
            if num_points_new != ga_manager.num_points:
                ga_manager.num_points = num_points_new
                running_ga = False
                ga_manager.reset_state()
            
            num_generations_new = slider_generations.handle_event(event)
            if num_generations_new != ga_manager.num_generations:
                ga_manager.num_generations = num_generations_new
                running_ga = False
                ga_manager.reset_state()

            if button_reload.is_clicked(event):
                running_ga = False
                ga_manager.reset_state()
            
            if button_run_ga.is_clicked(event):
                running_ga = not running_ga
            
        if running_ga:
            ga_manager.evolve_one_step()
        
        screen.fill(PALETTE["background"])
        
        # Desenha a UI
        pygame.draw.rect(screen, PALETTE["secondary"], (0, 70, width, UI_PANEL_HEIGHT))
        draw_text(screen, title_text, (width // 2, 40), font_size=48, color=PALETTE["text_dark"])
        button_reload.draw()
        button_run_ga.draw()
        slider_cities.draw()
        slider_generations.draw()
        
        draw_text(screen, f"Cidades: {ga_manager.num_points}", (180, 85), color=PALETTE["text_dark"])
        draw_text(screen, f"Gerações: {ga_manager.generation}/{ga_manager.num_generations}", (480, 85), font_size=20, color=PALETTE["text_dark"])
        
        best_dist = 1/ga_manager.best_individual.fitness if ga_manager.best_individual and ga_manager.best_individual.fitness > 0 else 0
        draw_text(screen, f"Melhor Distância: {best_dist:.2f}", (900, 160), font_size=20, color=PALETTE["text_dark"])

        draw_graph(screen, ga_manager.best_fitness_history, chart_area, PALETTE["primary"], "Melhor Aptidão")
        
        draw_points(screen, ga_manager.points)
        if ga_manager.best_individual:
            draw_route(screen, ga_manager.best_individual.route, ga_manager.points, PALETTE["primary"], thickness=3)
        
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    main()