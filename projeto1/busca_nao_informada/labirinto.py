from collections import deque

def definir_labirinto_grafo():
    """
    Representação do labirinto 7x9 do relatório (Figura 1) como lista de adjacências.
    Cada coordenada (linha, coluna) é um nó e as passagens livres são as arestas.
    """
    return {
        # Linha 0
        (0, 0): [(1, 0)],
        (0, 1): [(1, 1), (0, 2)],
        (0, 2): [(0, 1)],
        (0, 3): [(1, 3)],
        (0, 4): [(0, 5)],
        (0, 5): [(0, 4), (0, 6)],
        (0, 6): [(1, 6), (0, 7), (0, 5)],
        (0, 7): [(0, 6), (0, 8)],
        (0, 8): [(1, 8), (0, 7)],

        # Linha 1
        (1, 0): [(0, 0), (1, 1)],
        (1, 1): [(0, 1), (1, 2)],
        (1, 2): [(1, 1), (1, 3)],
        (1, 3): [(0, 3), (1, 2), (1, 4)],
        (1, 4): [(1, 5), (2, 4), (1, 3)],
        (1, 5): [(2, 5), (1, 4), (1, 6)],
        (1, 6): [(0, 6), (1, 5)],
        (1, 7): [(1, 8)],
        (1, 8): [(2, 8), (0, 8), (1, 7)],

        # Linha 2
        (2, 0): [(3, 0), (2, 1)],
        (2, 1): [(1, 1), (2, 0)],
        (2, 2): [(3, 2), (2, 3)],
        (2, 3): [(2, 2), (2, 4)],
        (2, 4): [(1, 4), (3, 4)],
        (2, 5): [(3, 6)],
        (2, 6): [(2, 7), (3, 6)],
        (2, 7): [(2, 6), (2, 8)],
        (2, 8): [(1, 8), (3, 8), (2, 7)],

        # Linha 3
        (3, 0): [(4, 0), (2, 0)],
        (3, 1): [(4, 1)],
        (3, 2): [(2, 2)],
        (3, 3): [(3, 4)],
        (3, 4): [(2, 4), (3, 5), (3, 3)],
        (3, 5): [(3, 4), (2, 5)],
        (3, 6): [(2, 6), (3, 7)],
        (3, 7): [(3, 6), (4, 7)],
        (3, 8): [(2, 8)],

        # Linha 4
        (4, 0): [(3, 0), (5, 0)],
        (4, 1): [(5, 1), (3, 1), (4, 2)],
        (4, 2): [(4, 1), (4, 3)],
        (4, 3): [(5, 3), (4, 2), (4, 4)],
        (4, 4): [(4, 5), (4, 3)],
        (4, 5): [(4, 4), (5, 5)],
        (4, 6): [(5, 6)],
        (4, 7): [(3, 7), (4, 8)],
        (4, 8): [(4, 7), (5, 8)],

        # Linha 5
        (5, 0): [(4, 0), (6, 0)],
        (5, 1): [(4, 1), (6, 1)],
        (5, 2): [(5, 3)],
        (5, 3): [(5, 2), (4, 3)],
        (5, 4): [(6, 4)],
        (5, 5): [(4, 5), (6, 5)],
        (5, 6): [(4, 6), (6, 6)],
        (5, 7): [(5, 8)],
        (5, 8): [(5, 7), (6, 8), (4, 8)],

        # Linha 6
        (6, 0): [(5, 0), (6, 1)],
        (6, 1): [(5, 1), (6, 0), (6, 2)],
        (6, 2): [(6, 3), (6, 1)],
        (6, 3): [(6, 2)],
        (6, 4): [(5, 4), (6, 5)],
        (6, 5): [(6, 6), (6, 4), (5, 5)],
        (6, 6): [(6, 5), (6, 7), (5, 6)],
        (6, 7): [(6, 6), (6, 8)],
        (6, 8): [(6, 7), (5, 8)]
    }


def obter_coordenada(prompt, default, max_linhas=6, max_colunas=8):
    """Lê uma coordenada no formato linha,coluna com validação e valor padrão."""
    while True:
        try:
            entrada = input(f"{prompt} [padrao: {default[0]},{default[1]}]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return default

        if not entrada:
            return default

        partes = entrada.split(',')
        if len(partes) != 2:
            print("Formato invalido. Digite no padrao 'linha,coluna' (ex: 0,0).")
            continue

        try:
            r = int(partes[0].strip())
            c = int(partes[1].strip())
            if not (0 <= r <= max_linhas and 0 <= c <= max_colunas):
                print(f"Coordenadas fora dos limites (linhas 0 a {max_linhas}, colunas 0 a {max_colunas}).")
                continue
            return (r, c)
        except ValueError:
            print("Entrada invalida. Digite numeros inteiros.")


def bfs(grafo, inicio, destino):
    """
    Busca em Largura (BFS) para encontrar o menor caminho entre 'inicio' e 'destino'.
    Garante o caminho de menor numero de passos em grafos sem pesos nas arestas.
    """
    fila = deque([(inicio, [inicio])])
    visitados = {inicio}

    while fila:
        atual, caminho = fila.popleft()

        if atual == destino:
            return caminho

        for vizinho in grafo.get(atual, []):
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, caminho + [vizinho]))

    return None


if __name__ == "__main__":
    labirinto = definir_labirinto_grafo()

    print("=== Busca em Largura (BFS) no Labirinto ===")
    print("Dimensoes: 7 linhas (0-6) x 9 colunas (0-8)\n")

    ponto_inicial = obter_coordenada("Posicao inicial (linha,coluna)", default=(0, 0))
    ponto_final = obter_coordenada("Posicao de destino (linha,coluna)", default=(6, 8))

    caminho = bfs(labirinto, ponto_inicial, ponto_final)

    if caminho:
        print("\nCaminho encontrado com sucesso!")
        print(" -> ".join(str(pos) for pos in caminho))
        print(f"Total de passos: {len(caminho) - 1}")
    else:
        print(f"\nNao existe caminho conectando {ponto_inicial} ate {ponto_final}.")