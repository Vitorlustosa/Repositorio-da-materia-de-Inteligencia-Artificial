# Projeto 1: Busca e Representação de Conhecimento

Módulo voltado à formulação de problemas em espaços de estados, busca heurística, dedução lógica e algoritmos evolucionários.

---

## Conteúdo do Módulo

1. **Busca Não Informada — Labirinto (`busca_nao_informada/labirinto.py`)**
   - **Técnica:** Busca em Largura (*Breadth-First Search* — BFS).
   - **Objetivo:** Encontrar o caminho mais curto (menor número de passos) entre duas coordenadas em um labirinto 7x9 modelado como grafo.

2. **Busca Informada — Mapa do DF (`busca_informada/mapa.py`)**
   - **Técnica:** Algoritmo A\* (*A-Star Search*) com fila de prioridades.
   - **Objetivo:** Calcular a rota de menor custo entre cidades do Distrito Federal combinando distância percorrida $g(n)$ e estimativa em linha reta $h(n)$.

3. **Busca Complexa — Sudoku (`busca_complexa/sudoku.py`)**
   - **Técnica:** *Backtracking* recursivo.
   - **Objetivo:** Preencher tabuleiros 9x9 de Sudoku testando valores válidos de 1 a 9 e retrocedendo ao atingir estados sem solução até o preenchimento completo.

4. **Satisfação de Restrições — Campo Minado (`csp/campominado.py`)**
   - **Técnica:** Dedução lógica por propagação de restrições (CSP).
   - **Objetivo:** Identificar com certeza minas (`M`) e casas seguras (`S`) com base no número de minas vizinhas das células reveladas.

5. **Algoritmo Genético — Jogo da Velha (`algoritmo_genetico/jogo_da_velha.py`)**
   - **Técnica:** Algoritmo Evolucionário vs Busca Adversária Minimax.
   - **Objetivo:** Evoluir uma população de agentes através de seleção por *fitness*, recombinação (*crossover*) e mutação para disputar um torneio contra um agente Minimax com chance de erro controlada.

6. **Banco de Conhecimento — Sistema Especialista (`banco_de_conhecimento/sistema_especialista.py`)**
   - **Técnica:** Sistema baseado em regras de produção e encadeamento direto (*forward chaining*).
   - **Objetivo:** Prescrever automaticamente rotinas de treino personalizadas avaliando nível, objetivo, frequência e restrições articulares.

---

## Como Executar

A partir da raiz do repositório:

```bash
# Labirinto (BFS)
python projeto1/busca_nao_informada/labirinto.py

# Mapa do DF (A*)
python projeto1/busca_informada/mapa.py

# Sudoku (Backtracking)
python projeto1/busca_complexa/sudoku.py

# Campo Minado (CSP)
python projeto1/csp/campominado.py

# Jogo da Velha (Genético vs Minimax)
python projeto1/algoritmo_genetico/jogo_da_velha.py

# Sistema Especialista de Treino
python projeto1/banco_de_conhecimento/sistema_especialista.py
```
