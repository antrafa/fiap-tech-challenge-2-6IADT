# Documentação Detalhada: `helpers.py`

O arquivo `helpers.py` funciona como uma "caixa de ferramentas" para o projeto. Ele agrupa uma variedade de funções utilitárias que são usadas em diferentes partes da aplicação, principalmente em `main.py`. A centralização dessas funções aqui mantém o código principal mais limpo e organizado.

## 1. Configuração Inicial

-   **`load_dotenv()`:** Carrega as variáveis de ambiente de um arquivo `.env`. Isso é usado especificamente para carregar a `OPENAI_API_KEY` de forma segura, sem expô-la diretamente no código.
-   **`PALETTE`:** Um dicionário que define a paleta de cores usada em toda a interface gráfica. Centralizar as cores aqui facilita a alteração do tema visual da aplicação, pois basta modificar os valores em um único lugar.

## 2. Geração de Dados

### `generate_points(n)`

-   **Propósito:** Criar o conjunto de dados para a simulação.
-   **Funcionamento:**
    1.  Gera uma lista de `n` dicionários, onde cada dicionário representa um ponto de entrega.
    2.  Para cada ponto, ele atribui aleatoriamente:
        -   Coordenadas `x` e `y` dentro da área do mapa.
        -   `priority`: 0 (regular) ou 1 (prioritário).
        -   `volume`: Um valor entre 1 e 10, representando o tamanho do pacote.
    -   Esta função é a fonte de todos os "problemas" que o algoritmo genético tentará resolver.

## 3. Funções de Desenho (Pygame)

Estas funções são a base para a renderização de todos os elementos visuais na tela do Pygame.

### `draw_points(screen, points)`

-   Percorre a lista de `points` e desenha um círculo para cada um na tela (`screen`).
-   A cor do círculo depende da `priority` do ponto, usando as cores definidas na `PALETTE`.

### `draw_legend(screen, position)`

-   Desenha uma pequena caixa com uma legenda explicando o significado das cores dos pontos (Prioritário vs. Regular).
-   Cria uma `Surface` semi-transparente para garantir que a legenda seja legível mesmo sobrepondo outros elementos do mapa.

### `draw_route(screen, route, points, color, thickness=2)`

-   Recebe uma `route` (uma lista de índices) e desenha as linhas que conectam os pontos na sequência correta.
-   Desenha a linha final conectando o último ponto de volta ao primeiro para fechar o ciclo.

### `draw_text(screen, text, position, ...)`

-   Uma função genérica para renderizar texto na tela. Ela lida com a criação da fonte, a renderização da superfície de texto e o posicionamento (centralizado ou alinhado à esquerda).

## 4. Integração com Matplotlib

### `convert_color(rgb_tuple)`

-   Uma pequena função de conversão. O Pygame usa cores no formato RGB (0-255), enquanto o Matplotlib usa um formato normalizado (0-1). Esta função faz a conversão necessária.

### `draw_plot(screen, history, rect, ...)`

-   **Propósito:** Renderizar o gráfico de evolução da aptidão.
-   **Funcionamento:**
    1.  **Verificação:** Se o histórico (`history`) estiver vazio, desenha um placeholder cinza com a mensagem "Aguardando simulação...".
    2.  **Criação do Gráfico:** Usa a biblioteca `matplotlib` para criar um gráfico de linhas (`ax.plot`) com as gerações no eixo X e a aptidão no eixo Y.
    3.  **Renderização para uma Superfície:** O truque aqui é que, em vez de mostrar o gráfico em uma janela separada (comportamento padrão do Matplotlib), ele é renderizado "fora da tela" em um buffer de imagem (`FigureCanvasAgg`).
    4.  **Conversão para Pygame:** Os dados brutos da imagem do gráfico são convertidos em uma `Surface` do Pygame.
    5.  **Desenho na Tela:** A superfície do gráfico é redimensionada para caber na `rect` designada e, finalmente, desenhada na tela principal da aplicação.

## 5. Geração de Relatório com IA

### `generate_llm_report(screen, width, height, best_individual, points)`

-   **Propósito:** Orquestrar todo o processo de geração de relatório usando a API da OpenAI.
-   **Passo a Passo:**
    1.  **Tela de Loading:** Imediatamente desenha um overlay semi-transparente e uma mensagem de "Gerando relatório..." na tela. Isso fornece feedback visual ao usuário de que a aplicação está ocupada e não travou (a chamada de API é síncrona e bloqueia a interface).
    2.  **Verificação da API Key:** Verifica se a `OPENAI_API_KEY` foi carregada do arquivo `.env`. Se não, exibe um erro no console e interrompe a função.
    3.  **Coleta e Preparação dos Dados:** Reúne todas as informações necessárias para a análise: a rota otimizada, os dados dos pontos, a distância total, o volume total e, crucialmente, calcula a distância de uma rota "ingênua" (sequencial) para servir como base de comparação de eficiência.
    4.  **Construção do Prompt:** Cria uma string de prompt longa e detalhada. O design do prompt é fundamental para o sucesso da função:
        -   **Define o Papel:** `"Você é um assistente de logística."`
        -   **Define a Tarefa:** `"Sua tarefa é gerar um relatório completo..."`
        -   **Define a Estrutura:** Exige explicitamente as seções que o relatório deve conter.
        -   **Fornece os Dados:** Insere todos os dados coletados em um formato claro e legível para o modelo.
    5.  **Chamada à API:** Cria um cliente `openai` e envia o prompt para o modelo `gpt-3.5-turbo` através do método `client.chat.completions.create()`.
    6.  **Tratamento de Erro:** Envolve a chamada à API em um bloco `try...except` para capturar e relatar possíveis falhas de conexão ou erros da API.
    7.  **Salvamento do Relatório:** Extrai o conteúdo da resposta do LLM, adiciona um título e salva tudo no arquivo `RELATORIO_DE_ROTA.md` com codificação `utf-8` para suportar todos os caracteres.
