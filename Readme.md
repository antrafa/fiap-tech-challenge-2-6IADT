# Tech Challenge - Otimização de Rotas com Algoritmos Genéticos

Este é o repositório do projeto "Tech Challenge - Fase 2", focado na otimização de rotas para distribuição de medicamentos e insumos hospitalares. O projeto utiliza algoritmos genéticos para resolver o problema do caixeiro viajante (TSP), buscando a rota mais curta e eficiente para as entregas.

O sistema também inclui uma visualização em tempo real das rotas otimizadas, desenvolvida com a biblioteca Pygame.

## Features

*   **Algoritmo Genético:** Implementação de um algoritmo genético para resolver o problema do caixeiro viajante (TSP).
*   **Operadores de GA:** Utiliza operadores de seleção por torneio, cruzamento OX1 e mutação por troca.
*   **Visualização em Tempo Real:** Interface gráfica com Pygame para visualizar o processo de otimização, a melhor rota encontrada e a evolução da aptidão.
*   **Interatividade:** Permite ajustar o número de cidades e de gerações em tempo real através de sliders.
*   **Penalidades:** O cálculo de aptidão inclui penalidades por excesso de capacidade do veículo e por não priorizar pontos de entrega importantes.

## Estrutura do Projeto

```
├───.gitignore
├───ga_classes.py         # Contém as classes `Individual` e `Population` do algoritmo genético.
├───helpers.py            # Funções auxiliares para desenho, geração de dados e conversão de cores.
├───main.py               # Ponto de entrada principal da aplicação, com o loop do Pygame.
├───map_background.png    # Imagem de fundo para o mapa.
├───Readme.md             # Este arquivo.
├───requirements.txt      # Dependências do projeto.
└───ui_elements.py        # Classes para os elementos de UI, como botões e sliders.
```

## Tecnologias Utilizadas

*   **Python 3**
*   **Pygame:** Para a interface gráfica e visualização.
*   **Matplotlib:** Para a plotagem do gráfico de evolução da aptidão.
*   **Numpy:** Para operações numéricas eficientes.

## Como Executar o Projeto

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### 1. Pré-requisitos

*   Python 3.x instalado.

### 2. Configurar o Ambiente Virtual

Recomendamos o uso de um ambiente virtual para isolar as dependências do projeto.

```bash
# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```

### 3. Instalar as Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias usando o `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Executar o Algoritmo e a Visualização

O código principal para a otimização e visualização está no arquivo `main.py`.

```bash
python main.py
```

Isso irá abrir uma janela do Pygame mostrando o processo de otimização. Utilize os sliders para ajustar o número de cidades e gerações, e os botões para controlar a simulação.

## Melhorias Futuras

*   Implementar outros operadores de cruzamento e mutação.
*   Adicionar mais restrições ao problema, como janelas de tempo para entrega.
*   Permitir a importação de dados de pontos de entrega de um arquivo (CSV, JSON, etc.).
