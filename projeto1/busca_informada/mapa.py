import heapq

# Grafo com distâncias reais aproximadas (em km) entre Regiões Administrativas do DF
GRAFO_DF = {
    "Plano_Piloto": [("Aguas_Claras", 13.88), ("Guara", 8.75), ("Nucleo_Bandeirante", 9.87), ("Taguatinga", 14.58)],
    "Aguas_Claras": [("Plano_Piloto", 13.88), ("Guara", 5.53), ("Planaltina", 35.82)],
    "Guara": [("Plano_Piloto", 8.75), ("Aguas_Claras", 5.53), ("Sobradinho", 25.23)],
    "Nucleo_Bandeirante": [("Plano_Piloto", 9.87), ("Taguatinga", 5.45)],
    "Taguatinga": [("Plano_Piloto", 14.58), ("Ceilandia", 10.12), ("Brazlandia", 32.58), ("Nucleo_Bandeirante", 5.45)],
    "Ceilandia": [("Taguatinga", 10.12), ("Gama", 11.96), ("Samambaia", 21.12)],
    "Brazlandia": [("Taguatinga", 32.58), ("Sobradinho", 19.57)],
    "Gama": [("Ceilandia", 11.96), ("Samambaia", 10.22)],
    "Samambaia": [("Ceilandia", 21.12), ("Gama", 10.22)],
    "Planaltina": [("Aguas_Claras", 35.82), ("Sobradinho", 14.51)],
    "Sobradinho": [("Guara", 25.23), ("Brazlandia", 19.57), ("Planaltina", 14.51)]
}

# Heurística h(n): estimativa em linha reta até o Plano Piloto (admissível para o destino central)
HEURISTICA_PLANO = {
    "Plano_Piloto": 0.0,
    "Taguatinga": 12.81,
    "Ceilandia": 21.21,
    "Gama": 27.73,
    "Samambaia": 30.41,
    "Aguas_Claras": 11.31,
    "Guara": 7.21,
    "Sobradinho": 19.70,
    "Planaltina": 28.28,
    "Brazlandia": 21.54,
    "Nucleo_Bandeirante": 8.49
}


def a_estrela(inicio, destino, grafo, heuristica):
    """
    Algoritmo de busca A* (A-Star).
    Minimiza f(n) = g(n) + h(n), onde:
      g(n): custo real acumulado do início até n
      h(n): estimativa heurística até o objetivo
    """
    # Fila de prioridade armazena tuplas: (f_score, g_score, no_atual, no_pai)
    h_inicio = heuristica.get(inicio, 0.0) if destino == "Plano_Piloto" else 0.0
    fila_prioridade = [(h_inicio, 0.0, inicio, None)]

    veio_de = {}
    custo_g = {inicio: 0.0}
    visitados = set()

    while fila_prioridade:
        f, g, atual, pai = heapq.heappop(fila_prioridade)

        if atual in visitados:
            continue

        veio_de[atual] = pai
        visitados.add(atual)

        if atual == destino:
            # Reconstrói a rota percorrendo os pais até a origem
            rota = []
            curr = atual
            while curr:
                rota.append(curr)
                curr = veio_de[curr]
            rota.reverse()
            return rota, g

        for vizinho, distancia in grafo.get(atual, []):
            if vizinho in visitados:
                continue

            novo_g = g + distancia
            if novo_g < custo_g.get(vizinho, float('inf')):
                custo_g[vizinho] = novo_g
                # Usa heurística se o destino for Plano Piloto, senão 0 (equivalente a Dijkstra)
                h_val = heuristica.get(vizinho, 0.0) if destino == "Plano_Piloto" else 0.0
                f_novo = novo_g + h_val
                heapq.heappush(fila_prioridade, (f_novo, novo_g, vizinho, atual))

    return None, float('inf')


def obter_ponto(mensagem, default):
    try:
        entrada = input(f"{mensagem} [padrao: {default}]: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return default
    return entrada if entrada else default


if __name__ == "__main__":
    print("=== Planejador de Rotas no Distrito Federal (Busca A*) ===")
    print("Regiões disponíveis:")
    for cidade in sorted(GRAFO_DF.keys()):
        print(f"  - {cidade}")

    origem = obter_ponto("\nDigite o ponto de partida", default="Samambaia")
    destino = obter_ponto("Digite o ponto de destino", default="Plano_Piloto")

    if origem not in GRAFO_DF or destino not in GRAFO_DF:
        print(f"\nErro: Cidade nao reconhecida no mapa. Verifique a grafia.")
    else:
        rota, custo_total = a_estrela(origem, destino, GRAFO_DF, HEURISTICA_PLANO)

        if rota:
            print("\nRota otimizada encontrada:")
            print(" -> ".join(rota))
            print(f"Distancia total estimada: {custo_total:.2f} km")
        else:
            print(f"\nNenhum caminho encontrado entre {origem} e {destino}.")
