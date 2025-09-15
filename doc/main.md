# Documentação Detalhada: `main.py`

`main.py` é o coração da aplicação, responsável por orquestrar todos os componentes: a lógica do algoritmo genético, a interface do usuário e o gerenciamento de eventos. Ele atua como o ponto de entrada que inicializa o Pygame e executa o loop principal da simulação.

## 1. Inicialização e Configuração

O arquivo começa importando as bibliotecas e módulos necessários e, em seguida, define as configurações iniciais da aplicação.

### Importações

-   `pygame` e `sys`: Para a criação da janela, manipulação de eventos e encerramento da aplicação.
-   Funções de `helpers`: Funções auxiliares para desenhar texto, pontos, rotas, o gráfico e a legenda.
-   Classes de `ui_elements`: `Button` e `Slider` para criar os controles interativos.
-   `Population` de `ga_classes`: A classe principal do algoritmo genético.

### Configuração da Janela e Layout

-   **Inicialização do Pygame:** `pygame.init()` prepara os módulos do Pygame para uso.
-   **Criação da Tela:** Uma janela de `1000x1000` pixels é criada.
-   **Constantes de Layout:** O código define uma série de constantes para organizar a interface de forma responsiva. Isso inclui as posições e dimensões do painel de UI, dos botões, dos sliders e das áreas do gráfico e do mapa. Essa abordagem torna mais fácil ajustar o layout no futuro.

### Inicialização dos Parâmetros e Elementos de UI

-   **Parâmetros Iniciais:** Define os valores padrão para a simulação (nº de pontos, gerações, etc.).
-   **Criação dos Elementos:** Cada botão e slider é instanciado com suas respectivas posições, dimensões, intervalos de valores e valores iniciais. Por exemplo:
    ```python
    # Cria o botão para iniciar/pausar a simulação
    button_run_ga = Button((BUTTON_RUN_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), "Rodar GA", "run")

    # Cria o slider para controlar o número de cidades
    slider_cities = Slider(SLIDER_X_COL1, SLIDER_Y_ROW1, SLIDER_WIDTH, SLIDER_HEIGHT, 2, 200, initial_num_points)
    ```
-   **Áreas de Desenho:** `pygame.Rect` é usado para definir as áreas retangulares onde o gráfico de aptidão e o mapa de rotas serão desenhados.

## 2. A Função Principal: `main()`

Esta função contém a lógica central da aplicação e o loop principal que a mantém em execução.

### Variáveis de Estado

-   A função começa inicializando as variáveis que controlarão o estado da simulação, como `num_points`, `num_generations`, `population_size`, e `mutation_rate`.
-   `points`: Armazena a lista de cidades (pontos de entrega) gerada pela função `generate_points()`.
-   `current_population`: Uma instância da classe `Population` é criada, representando a coleção inicial de rotas aleatórias.
-   `running` e `running_ga`: Flags booleanas que controlam o loop principal da aplicação e o estado de execução do algoritmo genético (rodando ou pausado).

### O Loop Principal (`while running`)

Este é o ciclo que mantém a janela aberta e a aplicação responsiva. A cada iteração, ele executa duas tarefas principais: **gerenciamento de eventos** e **atualização da tela**.

#### Gerenciamento de Eventos (`for event in pygame.event.get()`)

Esta parte do código verifica todas as interações do usuário:

1.  **Fechar a Janela:** Se o usuário clica no botão de fechar, a flag `running` se torna `False`, e o loop termina.
2.  **Interação com Sliders:** Para cada slider, a função `handle_event(event)` é chamada. Se o valor de um slider for alterado, a variável de estado correspondente é atualizada. Se a mudança afeta a estrutura da simulação (como o número de cidades ou o tamanho da população), a simulação do AG é reiniciada para refletir os novos parâmetros.
3.  **Interação com Botões:** O código verifica se algum botão foi clicado usando o método `is_clicked(event)`.
    -   `button_reload`: Reinicia a simulação.
    -   `button_run_ga`: Alterna o estado da flag `running_ga` (pausa ou continua).
    -   `button_regenerate`: Gera um novo conjunto de pontos.
    -   `button_generate_report`: Chama a função `generate_llm_report()` para criar o relatório com IA.

#### Lógica de Evolução do Algoritmo Genético

-   Após o tratamento de eventos, uma verificação é feita:
    ```python
    if running_ga and generation < num_generations:
    ```
-   Se o AG estiver rodando e o número máximo de gerações não tiver sido atingido, o método `current_population.evolve()` é chamado. Este é o comando que executa uma única geração de evolução (seleção, cruzamento e mutação).
-   Após a evolução, o `current_best_individual` é atualizado e sua aptidão é registrada no `best_fitness_history`.

#### Atualização da Tela

-   Ao final de cada iteração do loop, a função `print_screen()` é chamada. Ela é responsável por limpar a tela e redesenhar todos os elementos com base no estado atual da simulação.

## 3. A Função de Desenho: `print_screen()`

Esta função é dedicada exclusivamente a renderizar a interface gráfica. Recebe como parâmetros todas as variáveis de estado necessárias para desenhar a cena.

### Ordem de Desenho

1.  **Fundo:** A tela é preenchida com uma cor de fundo sólida.
2.  **Painel de UI:** Um retângulo é desenhado para servir como fundo para os controles.
3.  **Títulos e Textos:** O título principal e os valores atuais dos sliders e da simulação (geração, melhor distância, etc.) são renderizados.
4.  **Lógica dos Botões:** Antes de desenhar, a função atualiza o estado dos botões. Por exemplo, o texto do botão "Rodar GA" muda para "Pausar" quando a simulação está ativa, e o botão "Gerar Relatório" é desabilitado enquanto o AG não termina.
5.  **Desenho dos Elementos:** Os botões e sliders são desenhados na tela.
6.  **Gráfico e Mapa:** As funções `draw_plot()` e `draw_route()` são chamadas para renderizar as visualizações de dados nas áreas designadas.
7.  **Atualização Final:** `pygame.display.flip()` atualiza a tela inteira com tudo o que foi desenhado, e `pygame.time.wait(10)` introduz uma pequena pausa para controlar a taxa de quadros.

## 4. Ponto de Entrada

O bloco final do arquivo garante que a função `main()` seja chamada apenas quando o script é executado diretamente.

```python
if __name__ == '__main__':
    main()
```
