# Projeto 3: Aprendizado de Máquina e Deep Learning

Módulo dedicado aos paradigmas de aprendizado supervisionado, não supervisionado, por reforço e redes neurais profundas.

---

## Conteúdo do Módulo

1. **Regressão Linear — Aprendizado Supervisionado (`aprendizado_supervisionado.py`)**
   - **Técnica:** Regressão Linear Simples via Scikit-Learn.
   - **Objetivo:** Prever o consumo de energia elétrica residencial (em kWh) em função da variação da temperatura média diária (°C), avaliando o modelo com as métricas $R^2$ e RMSE e visualização gráfica da reta ajustada.

2. **Clusterização K-Means — Aprendizado Não Supervisionado (`aprendizado_nao_supervisionado.py`)**
   - **Técnica:** Padronização z-score (`StandardScaler`) e agrupamento K-Means ($k=3$).
   - **Objetivo:** Agrupar 18 países em blocos socioeconômicos comparando o PIB per capita e a Expectativa de Vida, identificando padrões de desenvolvimento global.

3. **Q-Learning no Buckshot Roulette — Aprendizado por Reforço (`aprendizado_por_reforco.py`)**
   - **Técnica:** Q-Learning tabular com *Action Masking* e *Reward Shaping*.
   - **Objetivo:** Treinar um agente autônomo para o jogo *Buckshot Roulette* (espingarda calibre 12 com cartuchos reais e de festim, itens como cano cerrado e algemas) para maximizar sua taxa de vitória contra um bot adversário.

4. **Transfer Learning — Deep Learning com PyTorch (`arquitetura_deep_learning.py`)**
   - **Técnica:** Rede Convolucional MobileNetV2 pré-treinada na ImageNet.
   - **Objetivo:** Classificação de imagens através de ajuste fino da camada classificadora linear final mantendo os blocos convolucionais congelados como extratores de atributos.

---

## Como Executar

A partir da raiz do repositório:

```bash
# Regressão Linear (Supervisionado)
python projeto3/aprendizado_supervisionado.py

# Clusterização K-Means (Não Supervisionado)
python projeto3/aprendizado_nao_supervisionado.py

# Q-Learning no Buckshot Roulette (Reforço)
python projeto3/aprendizado_por_reforco.py

# Transfer Learning com MobileNetV2 (Deep Learning)
python projeto3/arquitetura_deep_learning.py
```
