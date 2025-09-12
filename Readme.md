# Tech Challenge - Otimização de Rotas com Algoritmos Genéticos

Este é o repositório do projeto "Tech Challenge - Fase 2", focado na otimização de rotas para distribuição de medicamentos e insumos hospitalares. O projeto utiliza algoritmos genéticos para resolver o problema do caixeiro viajante (TSP), buscando a rota mais curta e eficiente para as entregas.

O sistema também inclui uma visualização em tempo real das rotas otimizadas, desenvolvida com a biblioteca Pygame.

## Requisitos do Projeto

* **Algoritmos Genéticos**: Implementação de um algoritmo genético para resolver o problema do TSP, com operadores de seleção, cruzamento e mutação.
* **Visualização Interativa**: Uso da biblioteca Pygame para visualizar o processo de otimização em tempo real.

## Como Executar o Projeto

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### 1. Configurar o Ambiente Virtual

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

### 2. Instalar as Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias usando o `requirements.txt`.

```bash
pip install -r requirements.txt
```
### 3. Executar o Algoritmo e a Visualização

O código principal para a otimização e visualização está no arquivo `main.py`.

```bash
python main.py
```

Isso irá abrir uma janela do Pygame mostrando o processo de otimização.
