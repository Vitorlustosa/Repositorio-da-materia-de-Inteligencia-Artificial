import random
from collections import Counter

# Probabilidade estimada de vitória em cada estado de compra no CS
PROB_VITORIA = {
    "ECO": 0.15,     # Pistolas básicas, chance baixa
    "HALF": 0.35,    # Submetralhadoras / scouts
    "FORCE": 0.30,   # Compra arriscada sem utilitários completos
    "FULL": 0.50     # Rifles principais (AK-47 / M4) e colete completo
}

# Matriz de transição de Markov: P(Próximo Estado | Estado Atual, Resultado)
# A decisão econômica depende unicamente do estado atual e se o time ganhou ou perdeu a rodada
TRANSICOES = {
    ("ECO", "win"):   {"HALF": 0.65, "FULL": 0.35},
    ("ECO", "lose"):  {"ECO": 1.00},

    ("HALF", "win"):  {"FULL": 0.80, "HALF": 0.20},
    ("HALF", "lose"): {"ECO": 0.85, "FORCE": 0.15},

    ("FULL", "win"):  {"FULL": 1.00},
    ("FULL", "lose"): {"HALF": 0.70, "FORCE": 0.30},

    ("FORCE", "win"): {"HALF": 0.50, "FULL": 0.50},
    ("FORCE", "lose"):{"ECO": 1.00}
}


def sortear_proximo_estado(distribuicao):
    """Sorteia o próximo estado de acordo com a distribuição de probabilidades fornecida."""
    estados = list(distribuicao.keys())
    pesos = list(distribuicao.values())
    return random.choices(estados, weights=pesos, k=1)[0]


def simular_rodada(estado_atual):
    """
    Simula uma rodada:
    1. Sorteia vitória ou derrota baseado na força do armamento (estado atual)
    2. Determina a transição para a próxima rodada seguindo a Cadeia de Markov
    """
    chance_win = PROB_VITORIA[estado_atual]
    resultado = "win" if random.random() < chance_win else "lose"

    regra_transicao = TRANSICOES[(estado_atual, resultado)]
    proximo_estado = sortear_proximo_estado(regra_transicao)

    return resultado, proximo_estado


def executar_simulacoes(rodadas=12, seed=42):
    random.seed(seed)
    estados_iniciais = ["ECO", "HALF", "FORCE", "FULL"]

    print("=" * 60)
    print("  Simulação da Economia do Counter-Strike (Cadeias de Markov)")
    print("=" * 60)

    for inicial in estados_iniciais:
        print(f"\n--- Cenário com Estado Inicial: {inicial} ---")
        estado = inicial
        historico_resultados = []
        historico_estados = [estado]

        for r in range(1, rodadas + 1):
            resultado, proximo = simular_rodada(estado)
            historico_resultados.append(resultado)
            status_txt = "Vitória " if resultado == "win" else "Derrota "
            print(f"  Round {r:2d}: Compra = {estado:<5} | Resultado = {status_txt} -> Próxima = {proximo}")
            estado = proximo
            historico_estados.append(estado)

        vitorias = historico_resultados.count("win")
        taxa_vit = (vitorias / rodadas) * 100
        contagem = Counter(historico_estados)

        print(f"  > Desempenho: {vitorias}/{rodadas} vitórias ({taxa_vit:.1f}%)")
        print(f"  > Estados mais frequentes: {dict(contagem.most_common(2))}")


if __name__ == "__main__":
    executar_simulacoes(rodadas=10)
