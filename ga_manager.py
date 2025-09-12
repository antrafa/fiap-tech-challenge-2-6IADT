import numpy as np
import random
from ga_classes import Population, Individual
from helpers import generate_points

class GeneticAlgorithmManager:
    def __init__(self, num_points, population_size, mutation_rate, num_generations):
        self.num_points = num_points
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.num_generations = num_generations
        self.points = []
        self.current_population = None
        self.best_individual = None
        self.generation = 0
        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.reset_state()

    def reset_state(self):
        self.points = generate_points(self.num_points)
        self.current_population = Population(self.population_size, self.points)
        self.best_individual = self.current_population.get_fittest()
        self.generation = 0
        self.best_fitness_history = []
        self.avg_fitness_history = []
    
    def evolve_one_step(self):
        if self.generation < self.num_generations:
            self.current_population.evolve(self.mutation_rate, self.points)
            self.best_individual = self.current_population.get_fittest()
            self.best_fitness_history.append(self.best_individual.fitness)
            self.avg_fitness_history.append(self.current_population.get_average_fitness())
            self.generation += 1