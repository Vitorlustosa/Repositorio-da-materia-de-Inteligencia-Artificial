from itertools import product

# Probabilidades a priori (taxa base de defeito histórico dos componentes)
PRIORIS = {
    "falha_RAM": 0.05,
    "falha_GPU": 0.05,
    "falha_placaMae": 0.05,
    "monitor_funciona": 0.95
}


# Modelagem das probabilidades condicionais P(Sintoma | Hipótese)
def prob_fans_giram(defeito_placa_mae: bool) -> float:
    # Se a placa-mãe queimou, os fans raramente recebem sinal (10%)
    return 0.10 if defeito_placa_mae else 0.99


def prob_emite_bipes(defeito_mobo: bool, defeito_ram: bool, defeito_gpu: bool) -> float:
    # Placa-mãe inoperante não consegue acionar o speaker do BIOS
    if defeito_mobo:
        return 0.01

    # Falhas em RAM ou placa de vídeo geram bipes característicos de alerta
    if defeito_ram and defeito_gpu:
        return 0.95
    if defeito_ram or defeito_gpu:
        return 0.90

    # Sistema saudável raramente bipa erro (5% de falso positivo)
    return 0.05


def calcular_probabilidade_conjunta(hipotese, evidencias):
    """
    Calcula P(Hipótese, Evidências) usando a regra do produto e independências condicionais.
    """
    prob = 1.0

    # 1. P(Causas): probabilidade a priori da combinação específica de componentes falharem
    for causa in ("falha_RAM", "falha_GPU", "falha_placaMae"):
        p_base = PRIORIS[causa]
        prob *= p_base if hipotese[causa] else (1.0 - p_base)

    # 2. P(Sintomas | Causas): verossimilhança das evidências observadas
    if "Fans_Giram" in evidencias:
        p_fans = prob_fans_giram(hipotese["falha_placaMae"])
        prob *= p_fans if evidencias["Fans_Giram"] else (1.0 - p_fans)

    if "PC_Gera_Bipes" in evidencias:
        p_bipe = prob_emite_bipes(
            hipotese["falha_placaMae"],
            hipotese["falha_RAM"],
            hipotese["falha_GPU"]
        )
        prob *= p_bipe if evidencias["PC_Gera_Bipes"] else (1.0 - p_bipe)

    if "monitor_funciona" in evidencias:
        p_mon = PRIORIS["monitor_funciona"]
        prob *= p_mon if evidencias["monitor_funciona"] else (1.0 - p_mon)

    return prob


def inferencia_por_enumeracao(evidencias):
    """
    Realiza inferência exaustiva:
    1. Percorre todas as 2^3 = 8 hipóteses possíveis de falhas (RAM, GPU, Placa-Mãe)
    2. Calcula P(H, E) para cada uma
    3. Normaliza pela evidência total (soma_conjunta)
    4. Marginaliza para encontrar P(Falha_i | E)
    """
    todas_hipoteses = []
    for ram, gpu, mobo in product([False, True], repeat=3):
        todas_hipoteses.append({
            "falha_RAM": ram,
            "falha_GPU": gpu,
            "falha_placaMae": mobo
        })

    conjuntas = [(hip, calcular_probabilidade_conjunta(hip, evidencias)) for hip in todas_hipoteses]
    soma_total = sum(p for _, p in conjuntas)

    marginais = {}
    for componente in ("falha_RAM", "falha_GPU", "falha_placaMae"):
        soma_causa = sum(p for hip, p in conjuntas if hip[componente])
        marginais[componente] = (soma_causa / soma_total) if soma_total > 0 else 0.0

    return marginais, soma_total


def obter_resposta_booleana(pergunta, default_sim=True):
    """Lê resposta de sim/não do usuário com suporte a valor padrão e EOF."""
    padrao_str = "S" if default_sim else "N"
    while True:
        try:
            resp = input(f"{pergunta} (s/n) [padrão: {padrao_str}]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return default_sim

        if not resp:
            return default_sim
        if resp in ['s', 'sim', 'y', 'yes', '1']:
            return True
        if resp in ['n', 'nao', 'não', 'no', '0']:
            return False

        print("Opção inválida. Digite 's' para sim ou 'n' para não.")


if __name__ == "__main__":
    print("=" * 60)
    print("  Diagnóstico Bayesiano de Falhas de Hardware (PC não liga)")
    print("=" * 60)
    print("Responda às observações do computador:\n")

    evidencias_coletadas = {
        "Fans_Giram": obter_resposta_booleana("1. Os ventiladores (fans/cooler) giram ao apertar o botão de ligar?", default_sim=True),
        "PC_Gera_Bipes": obter_resposta_booleana("2. Você ouve algum padrão de bipe emitido pela placa-mãe?", default_sim=True),
        "monitor_funciona": obter_resposta_booleana("3. O monitor foi testado e está funcionando normalmente?", default_sim=True)
    }

    marginais, _ = inferencia_por_enumeracao(evidencias_coletadas)

    nomes_formatados = {
        "falha_RAM": "Memória RAM",
        "falha_GPU": "Placa de Vídeo (GPU)",
        "falha_placaMae": "Placa-Mãe"
    }

    print("\n" + "=" * 45)
    print("      PROBABILIDADE POSTERIOR DE DEFEITO")
    print("=" * 45)
    for chave, prob in sorted(marginais.items(), key=lambda item: item[1], reverse=True):
        rotulo = nomes_formatados.get(chave, chave)
        barra = "#" * int(prob * 20)
        print(f"- {rotulo:<22}: {prob * 100:5.1f}%  [{barra:<20}]")

    principal_suspeito = max(marginais, key=marginais.get)
    print("-" * 45)
    print(f"Diagnostico mais provavel: {nomes_formatados[principal_suspeito]} ({marginais[principal_suspeito]*100:.1f}%)")
    print("=" * 45)
