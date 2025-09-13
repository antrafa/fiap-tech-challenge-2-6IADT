import random
import numpy as np
from math import sqrt

class Individual:
    """
    Representa uma única solução (uma rota) na população.

    Atributos:
        route (list): Uma lista de índices de pontos representando a ordem de visitação.
        points (list): Uma lista de todos os pontos possíveis, contendo seus dados.
        fitness (float): A pontuação de aptidão do indivíduo.
    """
    def __init__(self, route, points):
        """
        Inicializa um objeto Individual.

        Args:
            route (list): A rota para este indivíduo.
            points (list): A lista de todos os pontos.
        """
        self.route = route
        self.points = points
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        """
        Calcula a aptidão do indivíduo.

        A aptidão é inversamente proporcional ao custo total, que inclui a
        distância total da rota e penalidades por exceder a capacidade do veículo
        e por não priorizar pontos importantes.

        Returns:
            float: O valor da aptidão.
        """
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
        """
        Calcula a distância Euclidiana entre dois pontos.

        Args:
            point1 (tuple): As coordenadas do primeiro ponto (x, y).
            point2 (tuple): As coordenadas do segundo ponto (x, y).

        Returns:
            float: A distância Euclidiana.
        """
        return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

class Population:
    """
    Gerencia uma coleção de indivíduos (a população) para o algoritmo genético.

    Esta classe lida com a criação da população inicial e o processo de evolução,
    incluindo seleção, cruzamento e mutação.

    Atributos:
        population (list): Uma lista de objetos Individual.
    """
    def __init__(self, size, points):
        """
        Inicializa um objeto Population.

        Args:
            size (int): O número de indivíduos na população.
            points (list): A lista de todos os pontos possíveis.
        """
        self.population = []
        for _ in range(size):
            route = list(np.random.permutation(len(points)))
            self.population.append(Individual(route, points))

    def get_fittest(self):
        """
        Encontra o indivíduo com a maior aptidão na população.

        Returns:
            Individual: O indivíduo mais apto.
        """
        best_individual = self.population[0]
        for individual in self.population:
            if individual.fitness > best_individual.fitness:
                best_individual = individual
        return best_individual

    def get_average_fitness(self):
        """
        Calcula a aptidão média de toda a população.

        Returns:
            float: A aptidão média.
        """
        total_fitness = sum(ind.fitness for ind in self.population)
        return total_fitness / len(self.population)

    def select_parent_tournament(self, pool_size=5):
        """

        Seleciona um pai da população usando seleção por torneio.
        Um subconjunto aleatório da população é escolhido (o pool do torneio), e
        o indivíduo mais apto deste pool é selecionado como o pai.

        Args:
            pool_size (int): O número de indivíduos no torneio.

        Returns:
            Individual: O pai selecionado.
        """
        tournament_pool = random.sample(self.population, pool_size)
        fittest_parent = max(tournament_pool, key=lambda x: x.fitness)
        return fittest_parent

    def crossover_ox1(self, parent1, parent2):
        """
        Realiza o Crossover de Ordem (OX1) em dois pais para criar uma rota filha.

        Uma subsequência aleatória do primeiro pai é copiada para o filho.
        Os genes restantes são preenchidos a partir do segundo pai na ordem
        em que aparecem, evitando duplicatas.

        Args:
            parent1 (Individual): O primeiro pai.
            parent2 (Individual): O segundo pai.

        Returns:
            list: A rota filha resultante.
        """
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
        """
        Aplica mutação de troca a uma rota.

        Com uma probabilidade definida pela taxa de mutação, dois genes (pontos)
        na rota são trocados.

        Args:
            route (list): A rota a ser mutada.
            mutation_rate (float): A probabilidade de ocorrência de mutação.

        Returns:
            list: A rota mutada.
        """
        if random.random() < mutation_rate:
            idx1, idx2 = random.sample(range(len(route)), 2)
            route[idx1], route[idx2] = route[idx2], route[idx1]
        return route

    def evolve(self, mutation_rate, points):
        """
        Evolui a população para a próxima geração.

        Uma nova população é criada através de elitismo (preservando o melhor
        indivíduo), cruzamento e mutação.

        Args:
            mutation_rate (float): A taxa de mutação a ser usada para a nova geração.
            points (list): A lista de todos os pontos possíveis.
        """
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