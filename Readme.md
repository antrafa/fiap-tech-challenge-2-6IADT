# Otimização de Rotas com Algoritmo Genético e IA

**Tech Challenge - Fase 2**

**Autores:**
*   Ackeley Lennon (RM366072)
*   Antonio Rafael Ortega (RM365237)
*   Eduardo Tadeu Agarbella (RM366322)
*   Leandro Pessoa de Souza (RM365755)
*   Mateus Teixeira Castro (RM366469)

**Curso:** FIAP - IA para DEVS - 6IADT
**Data:** 14 de Outubro de 2025

---

## 1. Visão Geral

Este projeto é uma solução para o **Problema do Caixeiro Viajante (TSP)**, focado na otimização de rotas de entrega. Utilizando um **Algoritmo Genético** implementado em Python, a aplicação busca a rota mais eficiente (menor distância) para visitar uma série de pontos, respeitando restrições como capacidade de carga e prioridade de entrega.

A aplicação conta com uma **interface gráfica interativa**, desenvolvida com **Pygame**, que permite visualizar o processo de otimização em tempo real. O grande diferencial é a **integração com um Large Language Model (GPT-3.5)**, que gera automaticamente um relatório analítico da melhor rota encontrada.

<!-- Inserir um GIF ou Screenshot da aplicação aqui -->

## 2. Funcionalidades

-   **Núcleo de Otimização:**
    -   Implementação de um Algoritmo Genético com operadores de **Seleção por Torneio**, **Crossover de Ordem (OX1)** e **Mutação por Troca**.
    -   **Função de Aptidão Complexa:** Avalia as rotas com base na distância e aplica penalidades por excesso de capacidade do veículo e por não priorizar entregas urgentes.
-   **Interface Gráfica Interativa:**
    -   Visualização em tempo real da **melhor e segunda melhor rota** sobre um mapa.
    -   Gráfico que exibe a **evolução da aptidão** da melhor solução ao longo das gerações.
    -   Painel de controle com **sliders** para ajustar dinamicamente os parâmetros do AG (nº de cidades, nº de gerações, tamanho da população, taxa de mutação).
    -   Botões para controlar a execução da simulação (iniciar, pausar, reiniciar, gerar novos pontos).
-   **Integração com IA:**
    -   Funcionalidade de **"Gerar Relatório"** que utiliza a API da OpenAI para criar uma análise detalhada da rota otimizada.
    -   O relatório gerado em Markdown inclui instruções para o motorista, análise de eficiência e sugestões de melhoria.

## 3. Tecnologias Utilizadas

-   **Linguagem:** Python 3
-   **Interface Gráfica:** Pygame
-   **Computação Numérica:** Numpy
-   **Geração de Gráficos:** Matplotlib
-   **Integração com IA:** OpenAI
-   **Gestão de Ambiente:** Dotenv

## 4. Estrutura do Projeto

```
. 
├── doc/ # Documentação detalhada dos módulos 
│ ├── ga_classes.md 
│ ├── helpers.md 
│ ├── main.md 
│ ├── SUMARIO.md 
│ └── ui_elements.md 
├── .env_sample # Exemplo de arquivo para a chave da API 
├── ga_classes.py # Lógica do Algoritmo Genético 
├── helpers.py # Funções auxiliares (desenho, IA, etc.) 
├── main.py # Ponto de entrada e loop principal 
├── Readme.md # Este arquivo 
├── requirements.txt # Dependências do projeto 
└── ui_elements.py # Classes dos componentes de UI
```

## 5. Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto localmente.

### Pré-requisitos

-   Python 3.8 ou superior.

### Passo 1: Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_DIRETORIO>
```

### Passo 2: Configurar o Ambiente Virtual

É altamente recomendável usar um ambiente virtual para isolar as dependências.

```bash
# Criar o ambiente
python -m venv venv

# Ativar o ambiente
# No Windows:
# venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```

### Passo 3: Instalar as Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Configurar a Chave da API da OpenAI

Para usar a funcionalidade de geração de relatório com IA, você precisa de uma chave da API da OpenAI.

1.  Renomeie o arquivo `.env_sample` para `.env`.
2.  Abra o arquivo `.env` e adicione sua chave:

    ```
    OPENAI_API_KEY="sua_chave_secreta_aqui"
    ```

### Passo 5: Executar a Aplicação

```bash
python main.py
```

## 6. Como Usar

1.  **Ajuste os Parâmetros:** Use os sliders para configurar a complexidade do problema e os parâmetros do algoritmo.
2.  **Inicie a Simulação:** Clique em **"Rodar GA"** para iniciar o processo de otimização.
3.  **Observe a Evolução:** Acompanhe a melhoria da rota no mapa e a curva de aptidão no gráfico.
4.  **Gere o Relatório:** Ao final da simulação (quando o número de gerações for atingido), o botão **"Gerar Relatório"** ficará ativo. Clique nele para que a IA analise a melhor rota e crie o arquivo `RELATORIO_DE_ROTA.md`.

## 7. Documentação Detalhada

Para uma análise aprofundada de cada módulo do projeto, consulte a documentação na pasta `doc/`. Comece pelo **[Sumário da Documentação](./doc/SUMARIO.md)**.