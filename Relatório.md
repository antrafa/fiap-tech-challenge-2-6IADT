# Relatório Técnico Detalhado: Otimização de Rotas com Algoritmo Genético e IA

**Tech Challenge - Fase 2**

**Autores:**
*   Ackeley Lennon (RM366072)
*   Antonio Rafael Ortega (RM365237)
*   Eduardo Tadeu Agarbella (RM366322)
*   Leandro Pessoa de Souza (RM365755)
*   Mateus Teixeira Castro (RM366469)

**Curso:** FIAP - IA para DEVS - 6IADT
**Data:** 14 de Outubro de 2025

## 1. Visão Geral do Projeto

Este projeto aborda um desafio clássico da logística, conhecido como o **Problema do Caixeiro Viajante (TSP)**. O objetivo é determinar a rota mais curta e eficiente para um veículo que precisa visitar uma série de pontos de entrega e retornar à sua origem.

Para solucionar este problema, o projeto utiliza uma abordagem de **Inteligência Artificial** baseada em **Algoritmos Genéticos (AG)**. Inspirado na teoria da evolução de Charles Darwin, o algoritmo simula a "sobrevivência do mais apto" para encontrar soluções ótimas ou quase ótimas em um tempo computacionalmente viável.

A aplicação foi desenvolvida em **Python** e conta com uma **interface gráfica interativa** construída com a biblioteca **Pygame**. Essa interface permite a visualização em tempo real do processo de otimização, exibindo as rotas, um gráfico de desempenho e permitindo o ajuste de parâmetros do algoritmo.

Como um diferencial, o projeto integra um **Large Language Model (LLM)**, especificamente o **GPT-3.5-Turbo da OpenAI**, para gerar automaticamente um relatório detalhado e analítico sobre a melhor rota encontrada, transformando os dados brutos em insights acionáveis.

## 2. Arquitetura e Estrutura do Código

O código foi modularizado para garantir a separação de responsabilidades, facilitando a manutenção e o entendimento.

-   `main.py`: Ponto de entrada da aplicação. Orquestra a interface gráfica, gerencia o loop de eventos do Pygame e inicia o processo de otimização.
-   `ga_classes.py`: Contém a lógica central do Algoritmo Genético. Define a classe `Individual` (uma única rota) e a classe `Population` (uma coleção de rotas que evolui).
-   `helpers.py`: Módulo utilitário que agrupa funções auxiliares, como desenho de elementos na tela, geração de dados de pontos, e a função `generate_llm_report` que lida com a integração com a API da OpenAI.
-   `ui_elements.py`: Define componentes de UI reutilizáveis, como `Button` e `Slider`, para a interface gráfica.
-   `requirements.txt`: Lista todas as dependências Python necessárias para executar o projeto.
-   `.env_sample`: Arquivo de exemplo que indica a necessidade de criar um arquivo `.env` para armazenar a chave da API da OpenAI (`OPENAI_API_KEY`).

## 3. A Interface Gráfica (UI)

A interface foi projetada para ser intuitiva, fornecendo controle total sobre a simulação e feedback visual claro.

### Painel de Controle

Localizado na parte superior, este painel contém:

-   **Sliders:**
    -   **Cidades:** Ajusta o número de pontos de entrega (de 2 a 200).
    -   **Gerações:** Define o número de ciclos de evolução que o algoritmo executará (de 10 a 2000).
    -   **População:** Controla o número de rotas em cada geração (de 10 a 200).
    -   **Mutação:** Define a probabilidade (de 1% a 50%) de uma rota sofrer uma pequena alteração aleatória.
-   **Botões:**
    -   **Reiniciar:** Reseta a simulação para a geração 0.
    -   **Gerar Cidades:** Cria um novo conjunto de pontos de entrega aleatórios.
    -   **Rodar GA / Pausar:** Inicia ou pausa o processo de otimização.
    -   **Gerar Relatório:** Fica habilitado ao final da simulação e aciona a geração do relatório pela IA.

### Visualização de Dados

-   **Mapa de Rotas (Direita):**
    -   Exibe os pontos de entrega em um mapa.
    -   Desenha a **melhor rota** encontrada em destaque (azul claro) e a **segunda melhor rota** (cinza), permitindo uma comparação visual da diversidade das boas soluções.
-   **Gráfico de Aptidão (Esquerda):**
    -   Plota a evolução da "aptidão" (qualidade) da melhor rota ao longo das gerações. Um gráfico ascendente indica que o algoritmo está aprendendo e encontrando rotas cada vez melhores.
-   **Legenda:**
    -   Identifica os pontos de entrega: **vermelho para prioritários** e **azul para regulares**.

## 4. O Algoritmo Genético (GA)

O núcleo do projeto é o Algoritmo Genético, que imita o processo de seleção natural.

-   **Indivíduo (`Individual`):** Representa uma única solução, ou seja, uma rota completa (uma permutação dos índices dos pontos). É o "cromossomo" do nosso problema.
-   **População (`Population`):** Uma coleção de `Individual`, ou seja, um conjunto de várias rotas possíveis que evoluirão juntas.

### Função de Aptidão (`calculate_fitness`)

A aptidão é a "nota" que cada rota recebe. O objetivo do algoritmo é maximizar essa nota. A nota é calculada como o inverso do custo total (`1 / (custo + 1)`), significando que rotas com menor custo têm maior aptidão.

O **custo** é a soma da **distância total** da rota mais as **penalidades** por quebrar regras.

-   **Penalidades (Restrições):**
    1.  **Capacidade de Carga:** Se a soma dos volumes dos itens nos pontos de uma rota excede a capacidade máxima do veículo (fixada em 50), uma penalidade é aplicada, proporcional ao excesso de volume.
        ```python
        if current_volume > max_capacity:
            penalty += (current_volume - max_capacity) * 100
        ```
    2.  **Prioridade de Entrega:** Pontos marcados como prioritários devem ser visitados no início da rota. Se um ponto prioritário aparece depois da 5ª posição na sequência, uma penalidade severa é aplicada para desencorajar fortemente essa solução.
        ```python
        if self.points[gene_index]['priority'] == 1:
            if i > 5: # i é a posição na rota
                penalty += priority_penalty_factor # 1000
            break
        ```

### Processo Evolutivo (`evolve`)

A cada geração, a população de rotas é substituída por uma nova, potencialmente melhor, através dos seguintes operadores genéticos:

1.  **Elitismo:** A melhor rota (`elite`) da geração atual é automaticamente copiada para a próxima geração. Isso garante que o melhor resultado encontrado até o momento nunca seja perdido.
2.  **Seleção (Seleção por Torneio):** Para escolher os "pais" que gerarão a próxima geração, o algoritmo realiza um torneio: um pequeno grupo de rotas é selecionado aleatoriamente, e a melhor delas é escolhida como um dos pais.
3.  **Cruzamento (Crossover - *Order Crossover OX1*):** Dois pais são combinados para criar um "filho". O OX1 copia um segmento da rota de um pai e preenche o restante com os pontos da rota do outro pai, na ordem em que aparecem, sem causar duplicatas.
4.  **Mutação (*Swap Mutation*):** Após o cruzamento, há uma pequena chance (definida pelo slider "Mutação") de que a rota filha sofra uma mutação: duas cidades em sua sequência são trocadas de lugar. Isso introduz novidade e ajuda o algoritmo a escapar de ótimos locais.

## 5. Integração com Large Language Model (LLM)

Esta é uma das funcionalidades mais inovadoras do projeto, conectando a otimização matemática com a análise de linguagem natural.

-   **Funcionalidade:** Ao final do processo de otimização, o botão **"Gerar Relatório"** se torna ativo.
-   **O Processo (`generate_llm_report`):**
    1.  **Acionamento:** O clique no botão dispara a função. Uma tela de "loading" é exibida, pois a chamada à API pode levar alguns segundos.
    2.  **Coleta de Dados:** A função coleta informações cruciais sobre a melhor rota encontrada: a sequência de pontos, a distância total, o volume total da carga e, para fins de comparação, a distância de uma rota ingênua (sequencial).
    3.  **Construção do Prompt:** Um prompt detalhado e estruturado é montado. Ele instrui o LLM (GPT-3.5-Turbo) a atuar como um "assistente de logística" e a gerar um relatório em formato Markdown com seções pré-definidas:
        -   Instruções para o motorista.
        -   Relatório de eficiência (comparando a rota otimizada com a não otimizada).
        -   Sugestões de melhoria.
        -   Perguntas e Respostas.
    4.  **Chamada à API:** Utilizando a biblioteca `openai`, o prompt é enviado ao modelo.
    5.  **Geração do Arquivo:** A resposta do LLM é recebida e salva em um novo arquivo chamado `RELATORIO_DE_ROTA.md`, que pode ser imediatamente consultado pelo usuário.

-   **Configuração:** Para que a funcionalidade opere, é necessário criar um arquivo `.env` na raiz do projeto e adicionar a chave da API da OpenAI:
    ```
    OPENAI_API_KEY="SUA_CHAVE_DA_API_AQUI"
    ```

## 6. Dependências e Como Executar

Para executar o projeto, siga os passos abaixo.

### Dependências

As principais bibliotecas utilizadas são:
- `pygame`: Para a interface gráfica.
- `numpy`: Para operações numéricas.
- `matplotlib`: Para a criação do gráfico de aptidão.
- `openai`: Para a integração com a API da OpenAI.
- `python-dotenv`: Para gerenciar as variáveis de ambiente.

A lista completa está no arquivo `requirements.txt`.

### Passos para Execução

1.  **Clone o Repositório:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_DIRETORIO>
    ```

2.  **Crie e Ative um Ambiente Virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    # venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure a Chave da API:**
    - Renomeie o arquivo `.env_sample` para `.env`.
    - Abra o arquivo `.env` e insira sua chave da API da OpenAI.

5.  **Execute a Aplicação:**
    ```bash
    python main.py
    ```

---

## Apêndice A: Links

O código-fonte completo e as instruções de execução estão disponíveis no seguinte repositório Git, e o vídeo de apresentação está publicado no YouTube:

-   **Link do Repositório:** [https://github.com/antrafa/fiap-tech-challenge-2-6IADT/](https://github.com/antrafa/fiap-tech-challenge-2-6IADT/)
-   **Link da Apresentação em vídeo:** [https://youtu.be/](https://youtu.be/)
