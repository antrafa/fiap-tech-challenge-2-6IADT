# Relatório Técnico Detalhado: Otimização de Rotas com Algoritmo Genético

## 1. Qual o objetivo deste projeto?

Imagine que você gerencia uma empresa de entregas. Todos os dias, você tem um caminhão que precisa entregar pacotes em vários pontos da cidade e voltar para o depósito. O seu desafio é: **qual a melhor rota para o motorista fazer todas as entregas gastando o mínimo de combustível e tempo?**

Este projeto resolve exatamente esse quebra-cabeça de logística. Ele usa uma técnica de inteligência artificial chamada **Algoritmo Genético** para descobrir a rota mais eficiente possível, levando em conta regras importantes do mundo real.

O programa permite que você veja o "raciocínio" do algoritmo em tempo real, através de uma interface gráfica interativa.

## 2. Como funciona a tela do programa?

A tela do programa é dividida em três partes para que você possa entender tudo o que está acontecendo. A criação dos elementos, como os botões e controles, é feita de forma modular.

Por exemplo, é assim que o programa cria um botão ou um controle deslizante. É como montar um painel com peças de LEGO, cada uma com sua função:

```python
# Exemplo de criação de um Botão e um Slider em main.py

button_run_ga = Button((100, 100, 100, 40), "Rodar GA", "run")

slider_mutation = Slider(200, 100, 150, 15, 0.01, 0.5, 0.05, is_float=True)
```

E no "cérebro" do programa, ele fica o tempo todo de olho para ver se você clicou ou arrastou algo:

```python
# Exemplo de como o programa reage aos seus comandos em main.py

for event in pygame.event.get():
    # Verifica se o valor do slider de mutação mudou
    slider_mutation.handle_event(event)

    # Verifica se o botão de "Rodar GA" foi clicado
    if button_run_ga.is_clicked(event):
        running_ga = not running_ga # Inicia ou pausa a simulação
```

## 3. O que é o "Algoritmo Genético"?

O cérebro por trás deste projeto é o Algoritmo Genético. Ele é inspirado na **teoria da evolução de Charles Darwin** e usa a ideia de "sobrevivência do mais apto" para encontrar a melhor solução.

Funciona assim:

#### Passo 1: A População de Indivíduos
Primeiro, o algoritmo cria centenas de "indivíduos". Cada indivíduo é simplesmente **uma rota completa**, ou seja, uma tentativa de solução para o problema. No código, cada rota é um "objeto" da classe `Individual`. Pense nela como uma ficha de dados para cada rota:

```python
# Em ga_classes.py, a "ficha de dados" de uma rota
class Individual:
    def __init__(self, route, points):
        self.route = route # A sequência de cidades
        self.points = points # Os dados de todas as cidades
        # A "nota" da rota é calculada assim que ela é criada
        self.fitness = self.calculate_fitness()
```

#### Passo 2: A Nota da Rota (Função de Aptidão)
Para saber se uma rota é "boa" ou "ruim", o algoritmo dá uma nota para cada uma. Chamamos essa nota de **"aptidão"** (ou *fitness*). Quanto menor a distância e as "multas", maior a nota.

O código que faz esse cálculo é o coração do algoritmo. Ele soma a distância total e as multas para gerar o custo. Depois, inverte esse valor para criar a "nota" (quanto maior, melhor).

```python
# Em ga_classes.py, a função que dá a "nota" para a rota
def calculate_fitness(self):
    total_distance = 0
    current_volume = 0
    penalty = 0
    # ... (cálculos de distância e volume) ...

    # Aplica as multas (ver próximo passo)
    if current_volume > max_capacity:
        penalty += (current_volume - max_capacity) * 100

    # ... (lógica da multa de prioridade) ...

    total_cost = total_distance + penalty
    return 1 / (total_cost + 1) # Inverte o custo para ter a nota
```

#### Passo 3: As Regras do Jogo (Restrições)
Uma boa rota não é apenas curta, ela precisa seguir as regras. Se uma rota quebra uma regra, ela recebe uma "multa" que diminui sua nota.

1.  **Capacidade do Caminhão:** O caminhão não pode carregar mais do que aguenta. No código, a "multa" por excesso de peso é calculada assim:

    ```python
    # Lógica da multa por capacidade
    if current_volume > max_capacity:
        penalty += (current_volume - max_capacity) * 100
    ```
    **Tradução:** Se o volume total for maior que a capacidade, a diferença é multiplicada por 100 e adicionada como multa.

2.  **Entregas Urgentes:** Entregas prioritárias devem ser feitas no começo. Esta é a regra no código:

    ```python
    # Lógica da multa por prioridade
    for i, gene_index in enumerate(self.route):
        if self.points[gene_index]['priority'] == 1:
            if i > 5: # Se a posição for depois da 6ª parada
                penalty += priority_penalty_factor # Adiciona uma multa gigante
            break
    ```
    **Tradução:** O programa verifica a posição (`i`) do ponto prioritário. Se for depois da 5ª posição, a rota recebe uma multa gigante de 1000 pontos.

#### Passo 4: A Evolução (Onde a Mágica Acontece)
O algoritmo cria novas "gerações" de rotas, onde cada nova geração tende a ser melhor que a anterior.

1.  **Seleção dos Pais:** O programa faz um "torneio" para escolher os pais. Veja como funciona no código:

    ```python
    # Em ga_classes.py, a função do "torneio"
    def select_parent_tournament(self, pool_size=5):
        # 1. Pega um punhado de 5 rotas aleatórias da população
        tournament_pool = random.sample(self.population, pool_size)
        # 2. Escolhe a rota com a maior "nota" (fitness) desse grupo
        fittest_parent = max(tournament_pool, key=lambda x: x.fitness)
        return fittest_parent
    ```

2.  **Criar Filhos (Cruzamento):** O cruzamento que combina as rotas dos pais é um processo inteligente para não repetir cidades:

    ```python
    # Em ga_classes.py, o cruzamento para gerar uma rota "filha"
    def crossover_ox1(self, parent1, parent2):
        child_route = [None] * len(parent1.route)
        # 1. Pega um pedaço aleatório da rota do pai 1
        start_pos, end_pos = sorted(random.sample(range(len(parent1.route)), 2))
        child_route[start_pos:end_pos+1] = parent1.route[start_pos:end_pos+1]
        
        # 2. Pega as cidades que faltam da rota do pai 2
        parent2_genes = [gene for gene in parent2.route if gene not in child_route]
        
        # 3. Junta tudo para formar a rota filha
        p2_idx = 0
        for i in range(len(child_route)):
            if child_route[i] is None:
                child_route[i] = parent2_genes[p2_idx]
                p2_idx += 1
        return child_route
    ```

3.  **Pequenas Mudanças (Mutação):** A mutação é a parte mais simples. O código apenas sorteia um número. Se for menor que a taxa de mutação, ele troca duas cidades de lugar:

    ```python
    # Em ga_classes.py, a função de mutação
    def mutate(self, route, mutation_rate):
        if random.random() < mutation_rate:
            # Seleciona dois índices aleatórios e troca seus valores
            idx1, idx2 = random.sample(range(len(route)), 2)
            route[idx1], route[idx2] = route[idx2], route[idx1]
        return route
    ```

4.  **Proteger o Melhor (Elitismo):** Todo o processo de evolução acontece no método `evolve`. Note como a primeira coisa que ele faz é encontrar a "elite" e garantir que ela sobreviva:

    ```python
    # Em ga_classes.py, o ciclo de evolução
    def evolve(self, mutation_rate, points):
        new_population = []
        # 1. Encontra a melhor rota da geração atual (a elite)
        elite = self.get_fittest()
        # 2. Garante que ela já vá para a próxima geração
        new_population.append(Individual(elite.route, points))

        # 3. Cria o resto da nova população com cruzamento e mutação
        while len(new_population) < len(self.population):
            parent1 = self.select_parent_tournament()
            parent2 = self.select_parent_tournament()
            # ... (chama crossover e mutate) ...
            new_population.append(Individual(child_route, points))
            
        self.population = new_population
    ```

## 4. Estrutura do Código

O projeto é modularizado para separar responsabilidades, facilitando a manutenção e o entendimento.

*   `main.py`: Ponto de entrada e orquestrador da aplicação. Contém o loop principal do Pygame.
*   `ga_classes.py`: Contém a lógica central do Algoritmo Genético (classes `Individual` e `Population`).
*   `ui_elements.py`: Define componentes de UI reutilizáveis (`Button`, `Slider`).
*   `helpers.py`: Módulo utilitário com funções auxiliares para desenho, geração de dados e a paleta de cores.
*   `RELATORIO.md`: Este arquivo de documentação.

## 5. Conclusão

No final, este projeto é uma forma visual e interativa de entender como a inteligência artificial, inspirada na natureza, pode ser usada para resolver problemas complexos do nosso dia a dia, como a logística de transportes. Ele transforma um problema matemático abstrato em algo que podemos ver, controlar e com o qual podemos experimentar.