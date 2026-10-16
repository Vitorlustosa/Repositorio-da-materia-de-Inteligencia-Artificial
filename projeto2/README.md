# Projeto 2: Tratamento de Incerteza

Módulo dedicado a métodos probabilísticos para tomada de decisão, simulação de processos estocásticos e estimação contínua sob ruído sensorial.

---

## Conteúdo do Módulo

1. **Diagnóstico de Hardware — Redes Bayesianas (`redes_bayesianas.py`)**
   - **Técnica:** Inferência bayesiana exaustiva por enumeração de hipóteses.
   - **Objetivo:** Determinar a probabilidade posterior de defeito em componentes de computador (Memória RAM, GPU ou Placa-Mãe) a partir de evidências incertas e sintomas relatados pelo usuário (ventoinhas girando, bipes de alerta e estado do monitor).

2. **Simulação de Economia no CS — Cadeias de Markov (`modelos_markovianos.py`)**
   - **Técnica:** Cadeia de Markov discreta em tempo e espaço de estados.
   - **Objetivo:** Simular as transições econômicas entre tipos de compra no Counter-Strike (`ECO`, `HALF`, `FORCE` e `FULL`). As probabilidades de transição dependem unicamente do estado atual e do desfecho do round (vitória ou derrota), satisfazendo a propriedade de Markov.

3. **Rastreamento de Trajetória 3D — Filtro de Kalman (`filtro_kalman.py`)**
   - **Técnica:** Filtro de Kalman tridimensional em duas fases (Predição e Atualização).
   - **Objetivo:** Atenuar o ruído de sensores imprecisos (GPS e altímetro) e reconstruir com alta fidelidade a trajetória de voo suave de um helicóptero, reduzindo significativamente o erro médio quadrático (RMSE).

---

## Como Executar

A partir da raiz do repositório:

```bash
# Diagnóstico de Hardware (Redes Bayesianas)
python projeto2/redes_bayesianas.py

# Simulação Econômica do CS (Cadeias de Markov)
python projeto2/modelos_markovianos.py

# Rastreamento de Trajetória 3D (Filtro de Kalman)
python projeto2/filtro_kalman.py
```
