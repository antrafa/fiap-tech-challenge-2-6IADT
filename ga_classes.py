import random
import numpy as np
from math import sqrt

class Individual:
    """Representa uma única rota (solução) na população do AG."""
    def __init__(self, route, points):
        """Inicializa um indivíduo com uma rota e calcula sua aptidão."""
        self.route = route
        self.points = points
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        """Calcula a aptidão da rota com base na distância e penalidades."""
        total_distance = 0
        max_capacity = 50 
        current_volume = 0
        priority_penalty_factor = 1000
        penalty = 0

        for i in range(len(self.route) - 1):
            point_a_data = self.points[self.route[i]]
            point_b_data = self.points[self.route[i+1]]
            total_distance += self.get_distance(point_a_data['coords'], point_b_data['coords'])
            current_volume += point_a_data['volume']
            
        total_distance += self.get_distance(self.points[self.route[-1]]['coords'], self.points[self.route[0]]['coords'])
        current_volume += self.points[self.route[-1]]['volume']

        if current_volume > max_capacity:
            penalty += (current_volume - max_capacity) * 100

        for i, gene_index in enumerate(self.route):
            if self.points[gene_index]['priority'] == 1:
                if i > 5:
                    penalty += priority_penalty_factor
                break

        total_cost = total_distance + penalty
        return 1 / (total_cost + 1)

    @staticmethod
    def get_distance(point1, point2):
        """Calcula a distância Euclidiana entre dois pontos."""
        return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

class Population:
    """Gerencia a coleção de indivíduos (rotas) e o processo evolutivo."""
    def __init__(self, size, points):
        """Cria uma população inicial de rotas aleatórias."""
        self.population = []
        for _ in range(size):
            route = list(np.random.permutation(len(points)))
            self.population.append(Individual(route, points))

    def get_fittest(self):
        """Retorna o indivíduo mais apto (melhor rota) da população."""
        best_individual = self.population[0]
        for individual in self.population:
            if individual.fitness > best_individual.fitness:
                best_individual = individual
        return best_individual

    def get_average_fitness(self):
        """Calcula a aptidão média de toda a população."""
        total_fitness = sum(ind.fitness for ind in self.population)
        return total_fitness / len(self.population)

    def select_parent_tournament(self, pool_size=5):
        """Seleciona um indivíduo para reprodução usando seleção por torneio."""
        tournament_pool = random.sample(self.population, pool_size)
        fittest_parent = max(tournament_pool, key=lambda x: x.fitness)
        return fittest_parent

    def crossover_ox1(self, parent1, parent2):
        """Realiza o crossover de ordem (OX1) para criar uma nova rota filha."""
        child_route = [None] * len(parent1.route)
        start_pos = random.randint(0, len(parent1.route) - 1)
        end_pos = random.randint(0, len(parent1.route) - 1)
        if start_pos > end_pos:
            start_pos, end_pos = end_pos, start_pos
        child_route[start_pos:end_pos+1] = parent1.route[start_pos:end_pos+1]
        parent2_genes = [gene for gene in parent2.route if gene not in child_route]
        child_route_filled = []
        p2_idx = 0
        for gene in child_route:
            if gene is None:
                child_route_filled.append(parent2_genes[p2_idx])
                p2_idx += 1
            else:
                child_route_filled.append(gene)
        return child_route_filled

    def mutate(self, route, mutation_rate):
        """Aplica mutação de troca em uma rota com base na taxa de mutação."""
        if random.random() < mutation_rate:
            idx1, idx2 = random.sample(range(len(route)), 2)
            route[idx1], route[idx2] = route[idx2], route[idx1]
        return route

    def evolve(self, mutation_rate, points):
        """Evolui a população para a próxima geração usando elitismo, crossover e mutação."""
        new_population = []
        elite = self.get_fittest()
        new_population.append(Individual(elite.route, points))
        while len(new_population) < len(self.population):
            parent1 = self.select_parent_tournament()
            parent2 = self.select_parent_tournament()
            child_route = self.crossover_ox1(parent1, parent2)
            child_route = self.mutate(child_route, mutation_rate)
            new_population.append(Individual(child_route, points))
        self.population = new_population