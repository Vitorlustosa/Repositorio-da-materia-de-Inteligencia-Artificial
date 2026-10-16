# Repositório de Inteligência Artificial (FGA0221)

Repositório dedicado aos trabalhos práticos e implementações da disciplina de **Inteligência Artificial (FGA0221)** da **Universidade de Brasília (UnB)** — Faculdade de Ciências e Tecnologia em Engenharia (FGA - Campus Gama).

---

## Estrutura do Repositório

O projeto é estruturado em três módulos temáticos principais:

```text
.
├── projeto1/                                  # Fundamentos de IA e Algoritmos de Busca
│   ├── busca_nao_informada/
│   │   └── labirinto.py                       # Busca em Largura (BFS) em labirinto 7x9
│   ├── busca_informada/
│   │   └── mapa.py                            # Busca A* para rotas no Distrito Federal
│   ├── busca_complexa/
│   │   └── sudoku.py                          # Backtracking para resolução de Sudoku 9x9
│   ├── csp/
│   │   └── campominado.py                     # Satisfação de Restrições no Campo Minado
│   ├── algoritmo_genetico/
│   │   └── jogo_da_velha.py                   # Algoritmo Genético vs Minimax no Jogo da Velha
│   └── banco_de_conhecimento/
│       └── sistema_especialista.py            # Sistema Especialista para recomendação de treinos
│
├── projeto2/                                  # Tratamento de Incerteza
│   ├── redes_bayesianas.py                    # Diagnóstico probabilístico de falhas de hardware
│   ├── modelos_markovianos.py                 # Simulação da economia do Counter-Strike com Cadeias de Markov
│   └── filtro_kalman.py                       # Rastreamento e atenuação de ruído 3D de helicóptero
│
├── projeto3/                                  # Aprendizado de Máquina (Machine Learning e Deep Learning)
│   ├── aprendizado_supervisionado.py          # Regressão Linear: Temperatura vs Consumo de Energia
│   ├── aprendizado_nao_supervisionado.py      # Agrupamento de Países com K-Means (PIB vs Expectativa de Vida)
│   ├── aprendizado_por_reforco.py             # Q-Learning no jogo Buckshot Roulette
│   └── arquitetura_deep_learning.py           # Transfer Learning com MobileNetV2 (PyTorch)
│
├── requirements.txt                           # Dependências e bibliotecas Python
├── .gitignore                                 # Configuração de exclusão de arquivos transitórios
└── README.md                                  # Documentação geral do repositório
```

---

## Descrição dos Projetos

### Projeto 1: Fundamentos de IA e Algoritmos de Busca

Este módulo explora as principais estratégias de busca em espaço de estados, raciocínio lógico e algoritmos evolucionários:

1. **Busca Cega (Não Informada) — `busca_nao_informada/labirinto.py`**
   - **Algoritmo:** Busca em Largura (*Breadth-First Search* — BFS).
   - **Problema:** Encontrar o trajeto mais curto entre duas coordenadas quaisquer em um labirinto bidimensional de dimensões 7x9.
   - **Metodologia:** O labirinto é modelado como um grafo não direcionado em que cada célula livre é um nó e as transições possíveis entre vizinhos ortogonais formam as arestas. O BFS utiliza uma fila FIFO (`collections.deque`) para explorar os nós camada por camada, garantindo matematicamente a rota ótima em número de passos em grafos sem pesos nas arestas.

2. **Busca Informada — `busca_informada/mapa.py`**
   - **Algoritmo:** Busca A\* (*A-Star Search*) com fila de prioridades (`heapq`).
   - **Problema:** Encontrar o caminho de menor custo de deslocamento entre Regiões Administrativas do Distrito Federal (Plano Piloto, Taguatinga, Águas Claras, Ceilândia, Samambaia, Gama, Sobradinho, Planaltina, Brazlândia, etc.).
   - **Metodologia:** O mapa é estruturado como um grafo ponderado por distâncias reais em quilômetros. A função de custo total combina o custo percorrido até o nó atual com a estimativa heurística admissível em linha reta até o destino central:
     $$f(n) = g(n) + h(n)$$
     onde $g(n)$ é a distância acumulada real e $h(n)$ é a distância euclidiana estimada.

3. **Busca Complexa / Satisfação de Restrições — `busca_complexa/sudoku.py`**
   - **Algoritmo:** Busca com Retrocesso (*Backtracking*).
   - **Problema:** Resolução exata de tabuleiros de Sudoku 9x9.
   - **Metodologia:** O algoritmo percorre as células vazias atribuindo sucessivamente dígitos de 1 a 9 que satisfaçam as restrições locais (sem repetição na linha, na coluna e no quadrante 3x3). Quando atinge um estado inconsistente onde nenhuma atribuição é viável, desfaz a escolha anterior (retrocesso) e explora caminhos alternativos até o preenchimento total.

4. **Satisfação de Restrições (CSP) — `csp/campominado.py`**
   - **Abordagem:** Dedução lógica determinística por propagação de restrições em matriz 9x9.
   - **Metodologia:** Cada célula numérica revelada $n$ impõe restrições sobre suas casas vizinhas ainda ocultas:
     - *Regra 1:* Se a diferença entre o número da célula e as minas já encontradas for igual ao total de casas vizinhas desconhecidas, todas essas casas vizinhas são identificadas como minas (`M`).
     - *Regra 2:* Se o número de minas encontradas atingir o valor da célula, todas as demais células vizinhas desconhecidas são marcadas como seguras (`S`).
     O ciclo dedutivo é executado de forma iterativa até alcançar um ponto fixo (estabilidade).

5. **Algoritmo Genético vs Minimax — `algoritmo_genetico/jogo_da_velha.py`**
   - **Abordagem:** Algoritmo Evolucionário vs Busca Adversária no Jogo da Velha 3x3.
   - **Metodologia:**
     - *Agente Genético (AG):* Uma população de agentes compete em partidas mútuas. A estratégia de cada agente é representada por seu cromossomo (dicionário de mapeamento de estado para ação). Os agentes com maior *fitness* (pontuados por vitórias, empates e penalizados por jogadas inválidas) são selecionados para cruzamento (*crossover*) e mutação estocástica.
     - *Agente Minimax:* Algoritmo de busca adversária ótima que explora a árvore recursiva de jogadas futuras maximizando o ganho próprio e minimizando o ganho do adversário. Possui taxa de erro ajustável para simular um jogador imperfeito.
     - O módulo inclui um torneio comparativo entre o melhor agente evoluído pelo AG contra o Minimax.

6. **Banco de Conhecimento / Sistema Especialista — `banco_de_conhecimento/sistema_especialista.py`**
   - **Abordagem:** Sistema baseado em regras de produção e encadeamento direto (*forward chaining*).
   - **Metodologia:** Modela uma base de fatos a partir de respostas do usuário (nível de experiência, objetivo fitness, disponibilidade de dias e restrições articulares). As regras de inferência processam esses fatos e geram uma prescrição automatizada contendo divisão de treino adequada (AB, ABC, ABCDEF ou Fullbody), orientações de intensidade e adaptações biomecânicas de segurança.

---

### Projeto 2: Tratamento de Incerteza

Este módulo foca na modelagem de sistemas estocásticos, diagnóstico probabilístico e filtragem contínua de sinais ruidosos:

1. **Diagnóstico de Falhas de Hardware com Inferência Bayesiana — `redes_bayesianas.py`**
   - **Problema:** Identificar o componente responsável por um computador que não inicializa (RAM, Placa de Vídeo / GPU ou Placa-Mãe) a partir de evidências incertas e incompletas observadas pelo usuário (rotação das ventoinhas, emissão de bipes sonoros da placa-mãe e integridade do monitor).
   - **Metodologia:** Realiza inferência exaustiva por enumeração sobre o espaço amostral de todas as combinações de falhas possíveis $\{ \text{V}, \text{F} \}^3$. O algoritmo calcula a probabilidade conjunta de cada hipótese com as evidências:
     $$P(H, E) = P(H) \times P(E \mid H)$$
     Em seguida, aplica a normalização pela evidência total $\sum P(H, E)$ e calcula as probabilidades marginais a posteriori $P(\text{Causa}_i \mid E)$, indicando o componente com maior verossimilhança de defeito.

2. **Simulação de Economia no Counter-Strike com Cadeias de Markov — `modelos_markovianos.py`**
   - **Problema:** Modelar a dinâmica de compras de equipamentos em partidas competitivas de Counter-Strike ao longo de sucessivas rodadas.
   - **Estados Econômicos:** `ECO` (poupança), `HALF` (compra parcial), `FORCE` (compra forçada) e `FULL` (compra completa de rifles e utilitários).
   - **Metodologia:** Cada estado possui uma probabilidade intrínseca de vitória $P(\text{win} \mid \text{estado})$. A transição para o estado da rodada seguinte obedece à propriedade de Markov (depende estritamente do estado atual e do desfecho de vitória ou derrota no round). O simulador executa séries temporais para cada estado inicial e relata as taxas de vitória e estabilidade econômica.

3. **Estimativa de Trajetória 3D com Filtro de Kalman — `filtro_kalman.py`**
   - **Problema:** Estimar a trajetória suave real de voo tridimensional de um helicóptero cujas leituras de sensores (GPS e altímetro) são contaminadas por ruído branco gaussiano.
   - **Metodologia:** Filtro de Kalman desacoplado nos eixos $X$, $Y$ e $Z$ operando recursivamente em dois estágios:
     1. *Predição da incerteza:* $P_k^- = P_{k-1} + Q$
     2. *Ganho de Kalman:* $K_k = \frac{P_k^-}{P_k^- + R}$
     3. *Atualização de estado:* $\hat{x}_k = \hat{x}_k^- + K_k (z_k - \hat{x}_k^-)$
     4. *Atualização da incerteza:* $P_k = (1 - K_k) P_k^-$
     O script compara graficamente em 3D as medições ruidosas contra a estimativa filtrada e calcula a redução do erro médio quadrático (RMSE).

---

### Projeto 3: Aprendizado de Máquina (Machine Learning e Deep Learning)

Este módulo abrange os paradigmas supervisionado, não supervisionado, por reforço e aprendizado profundo:

1. **Aprendizado Supervisionado (Regressão Linear) — `aprendizado_supervisionado.py`**
   - **Problema:** Modelar e prever o consumo elétrico residencial (em kWh) em função da temperatura média ambiente diária (°C).
   - **Metodologia:** Ajusta um modelo de Regressão Linear Simples via Scikit-Learn após particionamento em conjuntos de treino (80%) e teste (20%). O script avalia a relação física (aumento do consumo impulsionado pelo uso de refrigeração) e quantifica o desempenho por meio do $R^2$ (*Score* de Determinação) e RMSE, gerando gráficos de dispersão dos dados e visualização da reta ajustada.

2. **Aprendizado Não Supervisionado (Clusterização K-Means) — `aprendizado_nao_supervisionado.py`**
   - **Problema:** Agrupamento de 18 nações com base em dados de desenvolvimento humano: PIB per capita (USD) e Expectativa de Vida (anos).
   - **Metodologia:** Aplicação prévia de padronização z-score com `StandardScaler` (essencial para equilibrar as escalas numéricas distintas entre renda e longevidade) seguida pelo algoritmo K-Means ($k=3$). O script classifica os países em 3 blocos socioeconômicos bem delimitados e plota o diagrama de dispersão anotado com os nomes de cada país.

3. **Aprendizado por Reforço (Q-Learning) — `aprendizado_por_reforco.py`**
   - **Problema:** Treinar um agente autônomo para o jogo *Buckshot Roulette* (roleta russa com espingarda calibre 12 contendo cartuchos reais e de festim misturados, além de itens especiais como cano cerrado e algemas).
   - **Metodologia:** Implementação do algoritmo Q-Learning tabular atualizado via Equação de Bellman:
     $$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]$$
     - *Action Masking:* Garante que o agente selecione apenas ações válidas de acordo com seu inventário e o estado do tambor.
     - *Reward Shaping:* Recompensa a eliminação do oponente e jogadas táticas (ex.: disparar contra si com cartucho de festim para reter a vez de jogo), penalizando tiros reais contra si e desperdício de itens.
     - Avaliação final com política gulosa pura contra bot heurístico em 500 partidas.

4. **Deep Learning / Transfer Learning — `arquitetura_deep_learning.py`**
   - **Problema:** Classificação visual de raças de cães por meio de redes neurais convolucionais (CNNs).
   - **Metodologia:** Aplicação de *Transfer Learning* utilizando a arquitetura MobileNetV2 pré-treinada na base ImageNet (PyTorch/torchvision). Os pesos convolucionais profundos são congelados como extratores de características, substituindo-se a camada densa final pelo número de classes desejado. Inclui pipelines de aumento de dados (*Data Augmentation*) e rotina de validação e inferência pontual.

---

## Como Instalar e Executar

### Pré-requisitos
- Python 3.10 ou superior
- Gerenciador de pacotes `pip`

### 1. Clonar o Repositório e Criar Ambiente Virtual

```bash
# Clonar o repositório
git clone https://github.com/Vitorlustosa/Repositorio-da-materia-de-Inteligencia-Artificial.git
cd Repositorio-da-materia-de-Inteligencia-Artificial

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# No Windows (PowerShell):
.venv\Scripts\Activate.ps1
# No Linux / macOS:
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

---

### 2. Executando os Scripts

#### Executar Módulos do Projeto 1:
```bash
# Busca em Largura (Labirinto)
python projeto1/busca_nao_informada/labirinto.py

# Busca A* (Mapa do DF)
python projeto1/busca_informada/mapa.py

# Resolução de Sudoku (Backtracking)
python projeto1/busca_complexa/sudoku.py

# Campo Minado (CSP)
python projeto1/csp/campominado.py

# Algoritmo Genético vs Minimax (Jogo da Velha)
python projeto1/algoritmo_genetico/jogo_da_velha.py

# Sistema Especialista de Treinos
python projeto1/banco_de_conhecimento/sistema_especialista.py
```

#### Executar Módulos do Projeto 2:
```bash
# Diagnóstico de Hardware (Redes Bayesianas)
python projeto2/redes_bayesianas.py

# Simulação da Economia do Counter-Strike (Cadeias de Markov)
python projeto2/modelos_markovianos.py

# Rastreamento de Trajetória 3D (Filtro de Kalman)
python projeto2/filtro_kalman.py
```

#### Executar Módulos do Projeto 3:
```bash
# Regressão Linear (Aprendizado Supervisionado)
python projeto3/aprendizado_supervisionado.py

# Clusterização K-Means (Aprendizado Não Supervisionado)
python projeto3/aprendizado_nao_supervisionado.py

# Q-Learning no Buckshot Roulette (Aprendizado por Reforço)
python projeto3/aprendizado_por_reforco.py

# Transfer Learning com MobileNetV2 (Deep Learning)
python projeto3/arquitetura_deep_learning.py
```

---

## Autor

Desenvolvido por **Vitor Guilherme Lustosa de Carvalho**  
Faculdade de Ciências e Tecnologia em Engenharia — FGA / Universidade de Brasília (UnB)  
Disciplina: Inteligência Artificial (FGA0221)  
Professor: Fabiano Araujo Soares
