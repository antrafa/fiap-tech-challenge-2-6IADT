# Documentação Detalhada: `ui_elements.py`

O arquivo `ui_elements.py` é responsável por encapsular a lógica e o desenho de componentes de interface de usuário (UI) reutilizáveis. Ao criar classes para elementos como botões e sliders, o código em `main.py` se torna muito mais limpo e declarativo, focando em *o que* os elementos fazem, em vez de *como* eles são desenhados e gerenciados.

## 1. Classe `Button`

A classe `Button` cria um botão clicável com texto, que pode também ser desabilitado.

### `__init__(self, rect, text, action)`

-   **Propósito:** O construtor da classe.
-   **Parâmetros:**
    -   `rect`: Uma tupla ou `pygame.Rect` definindo a posição e o tamanho do botão (x, y, largura, altura).
    -   `text`: O texto que será exibido no botão.
    -   `action`: Uma string que serve como um identificador para a ação do botão (não é usada diretamente pela classe, mas ajuda a organizar a lógica em `main.py`).
-   **Atributos:**
    -   `self.rect`: O objeto `pygame.Rect` que representa a área do botão.
    -   `self.disabled`: Um booleano que controla o estado do botão. Se `True`, o botão não pode ser clicado e sua aparência muda.

### `draw(self, screen)`

-   **Propósito:** Desenhar o botão na tela.
-   **Funcionamento:**
    1.  **Verifica o Estado:** A cor de fundo (`bg_color`) e do texto (`text_color`) são escolhidas com base no estado do atributo `self.disabled`.
    2.  **Desenha a Sombra:** Um retângulo um pouco deslocado é desenhado primeiro para dar um efeito de profundidade (sombra).
    3.  **Desenha o Corpo e a Borda:** O retângulo principal do botão e sua borda são desenhados.
    4.  **Renderiza o Texto:** O texto do botão é renderizado e posicionado no centro do retângulo.

### `is_clicked(self, event)`

-   **Propósito:** Verificar se o botão foi clicado.
-   **Funcionamento:**
    1.  **Verifica se está Desabilitado:** Se `self.disabled` for `True`, retorna `False` imediatamente.
    2.  **Verifica o Evento:** Checa se o evento do mouse é um clique com o botão esquerdo (`event.type == pygame.MOUSEBUTTONDOWN and event.button == 1`).
    3.  **Verifica a Colisão:** Usa `self.rect.collidepoint(event.pos)` para ver se as coordenadas do clique do mouse estão dentro da área do botão.
    4.  Retorna `True` somente se todas as condições forem atendidas.

## 2. Classe `Slider`

A classe `Slider` cria um controle deslizante horizontal para selecionar um valor dentro de um intervalo.

### `__init__(self, x, y, w, h, min_val, max_val, initial_val, is_float=False)`

-   **Propósito:** O construtor da classe.
-   **Parâmetros:**
    -   `x, y, w, h`: Posição e dimensões da barra do slider.
    -   `min_val`, `max_val`: Os valores mínimo e máximo do intervalo.
    -   `initial_val`: O valor inicial do slider.
    -   `is_float`: Um booleano que determina se o slider deve retornar valores de ponto flutuante (`True`) ou inteiros (`False`).
-   **Atributos:**
    -   `self.rect`: O `pygame.Rect` da barra de fundo do slider.
    -   `self.handle_rect`: O `pygame.Rect` do controle deslizante (o quadrado que o usuário arrasta).
    -   `self.is_dragging`: Um booleano que rastreia se o usuário está atualmente arrastando o controle.

### `draw(self, screen)`

-   **Propósito:** Desenhar o slider na tela.
-   **Funcionamento:** Desenha a barra de fundo e o controle deslizante (`handle_rect`) em suas posições atuais.

### `handle_event(self, event)`

-   **Propósito:** Gerenciar toda a lógica de interação do usuário com o slider.
-   **Funcionamento:**
    1.  **Iniciar Arraste:** Se o usuário clica com o mouse (`MOUSEBUTTONDOWN`) sobre o controle (`handle_rect`), a flag `self.is_dragging` se torna `True`.
    2.  **Parar Arraste:** Se o usuário solta o botão do mouse (`MOUSEBUTTONUP`), `self.is_dragging` se torna `False`.
    3.  **Movimento do Mouse:** Se o mouse se move (`MOUSEMOTION`) *enquanto* `self.is_dragging` é `True`:
        a.  A posição horizontal do controle (`self.handle_pos`) é atualizada para a posição do mouse.
        b.  A posição é limitada para não ultrapassar os limites da barra do slider.
        c.  **O cálculo principal acontece aqui:** O valor (`self.val`) é calculado por interpolação linear. A posição do controle ao longo da barra é mapeada para o intervalo de valores (`min_val` a `max_val`).
        d.  Se `is_float` for `False`, o valor é arredondado para o inteiro mais próximo.
        e.  A posição do `handle_rect` é atualizada.
-   **Retorno:** A função sempre retorna o valor atual (`self.val`), permitindo que o código em `main.py` verifique e reaja a mudanças a cada quadro.
