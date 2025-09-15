# Documentação Detalhada: `ga_classes.py`

`ga_classes.py` é o arquivo que contém a implementação central do Algoritmo Genético. Ele define as estruturas de dados e a lógica que permitem a criação, avaliação e evolução das soluções para o problema de otimização de rotas.

## 1. Classe `Individual`

A classe `Individual` representa uma única solução candidata ao problema, ou seja, uma rota completa. No jargão dos algoritmos genéticos, um `Individual` é um "cromossomo".

### `__init__(self, route, points)`

-   **Propósito:** O construtor da classe. É chamado sempre que uma nova rota (indivíduo) é criada.
-   **Parâmetros:**
    -   `route`: Uma lista de inteiros que representa a sequência de visitação dos pontos (e.g., `[0, 3, 1, 2]`).
    -   `points`: A lista completa de dicionários de pontos, contendo os dados de coordenadas, prioridade e volume de cada um.
-   **Funcionamento:**
    1.  Armazena a `route` e os `points` como atributos do objeto.
    2.  Imediatamente chama o método `self.calculate_fitness()` para calcular a "nota" (aptidão) da rota assim que ela é criada e armazena o resultado em `self.fitness`.

### `calculate_fitness(self)`

-   **Propósito:** Este é o método mais crítico. Ele calcula a qualidade (aptidão) de uma rota. O objetivo do AG é maximizar esse valor.
-   **Funcionamento:**
    1.  **Cálculo da Distância e Volume:** O método percorre a rota, calculando a distância euclidiana entre cada par de pontos consecutivos e somando o volume da carga.
    2.  **Cálculo do Custo Total:** O custo é a soma da distância total com as penalidades.
    3.  **Aplicação de Penalidades (Restrições):**
        -   **Excesso de Capacidade:** Se `current_volume` ultrapassa `max_capacity` (50), uma penalidade é adicionada ao custo. A penalidade é proporcional ao excesso de volume, desencorajando rotas que sobrecarreguem o veículo.
        -   **Não Cumprimento de Prioridade:** O código verifica a posição do primeiro ponto prioritário na rota. Se ele não estiver entre as 6 primeiras paradas (`i > 5`), uma penalidade fixa e alta (`priority_penalty_factor = 1000`) é aplicada. Isso torna a rota extremamente "cara" e, portanto, muito pouco apta a sobreviver.
    4.  **Cálculo da Aptidão:** A aptidão é calculada como o inverso do custo total (`1 / (total_cost + 1)`). O `+ 1` evita divisão por zero. Essa inversão significa que rotas com **menor custo** terão **maior aptidão**.

### `get_distance(point1, point2)`

-   **Propósito:** Uma função estática (`@staticmethod`) simples que calcula a distância euclidiana entre dois pontos.

## 2. Classe `Population`

A classe `Population` gerencia uma coleção de indivíduos (`Individual`) e orquestra o processo evolutivo.

### `__init__(self, size, points)`

-   **Propósito:** Cria a população inicial de rotas.
-   **Funcionamento:** Gera `size` indivíduos, cada um com uma rota criada a partir de uma permutação aleatória dos índices dos pontos (`np.random.permutation`). Isso garante que a população inicial seja diversificada.

### Métodos de Avaliação

-   **`get_fittest(self)`:** Percorre toda a população e retorna o indivíduo com a maior aptidão (a melhor rota).
-   **`get_second_fittest(self)`:** Ordena a população pela aptidão em ordem decrescente e retorna o segundo elemento. Útil para visualização e análise da diversidade das soluções.
-   **`get_average_fitness(self)`:** Calcula e retorna a média de aptidão de todos os indivíduos na população.

### Operadores Genéticos

Estes são os métodos que impulsionam a evolução da população.

-   **`select_parent_tournament(self, pool_size=5)` (Seleção):**
    -   Implementa a **Seleção por Torneio**. Em vez de simplesmente escolher os melhores, este método seleciona um pequeno subconjunto aleatório da população (o `tournament_pool`) e retorna o melhor indivíduo *desse subconjunto*. Isso dá a indivíduos um pouco menos aptos uma chance de se reproduzir, aumentando a diversidade genética e evitando a convergência prematura para uma solução subótima.

-   **`crossover_ox1(self, parent1, parent2)` (Cruzamento):**
    -   Implementa o **Order Crossover (OX1)**, um método de cruzamento ideal para problemas baseados em permutação como o TSP.
    -   **Passo a Passo:**
        1.  Um trecho aleatório da rota do `parent1` é copiado diretamente para a rota filha (`child_route`).
        2.  Os pontos restantes são preenchidos com os genes do `parent2`, na ordem em que aparecem, pulando aqueles que já foram copiados do `parent1`.
        -   Este processo garante que a rota filha seja sempre válida (não contém cidades duplicadas).

-   **`mutate(self, route, mutation_rate)` (Mutação):**
    -   Implementa a **Mutação por Troca (Swap Mutation)**.
    -   Há uma pequena chance (`mutation_rate`) de que a mutação ocorra. Se ocorrer, dois pontos aleatórios na rota são escolhidos e suas posições são trocadas. A mutação é crucial para introduzir nova diversidade na população e evitar que o algoritmo fique "preso" em uma solução.

### `evolve(self, mutation_rate, points)`

-   **Propósito:** Executa um ciclo completo de evolução para criar a próxima geração.
-   **Funcionamento:**
    1.  **Elitismo:** A primeira coisa que ele faz é chamar `self.get_fittest()` para encontrar a melhor rota da geração atual. Essa rota (a "elite") é adicionada diretamente à `new_population`. Isso garante que a melhor solução encontrada até agora nunca seja perdida.
    2.  **Loop de Reprodução:** O método entra em um loop que continua até que a `new_population` atinja o mesmo tamanho da população original.
    3.  **Criação de Novos Indivíduos:** Dentro do loop, dois pais são selecionados usando `select_parent_tournament()`. Eles são combinados usando `crossover_ox1()` para criar uma rota filha, que por sua vez passa pelo processo de `mutate()`.
    4.  O novo indivíduo, com sua rota recém-criada, é instanciado e adicionado à `new_population`.
    5.  **Substituição:** Ao final do loop, a antiga população (`self.population`) é completamente substituída pela `new_population`.
