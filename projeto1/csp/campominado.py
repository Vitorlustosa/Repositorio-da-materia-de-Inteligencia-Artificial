from itertools import product

def obter_vizinhos(linha, col, tamanho=9):
    """Gera as coordenadas dos vizinhos válidos ao redor da célula (linha, col)."""
    for d_linha, d_col in product([-1, 0, 1], repeat=2):
        if d_linha == 0 and d_col == 0:
            continue
        viz_linha, viz_col = linha + d_linha, col + d_col
        if 0 <= viz_linha < tamanho and 0 <= viz_col < tamanho:
            yield viz_linha, viz_col


def resolver_campo_minado(tabuleiro):
    """
    Resolve deduções lógicas do campo minado aplicando restrições locais:
    1. Se (número da célula - minas já marcadas) == células ocultas ao redor -> todas são minas.
    2. Se minas já marcadas == número da célula -> todas as demais células ocultas são seguras.
    Itera até que nenhuma dedução adicional seja possível.
    """
    tamanho = len(tabuleiro)
    houve_mudanca = True

    while houve_mudanca:
        houve_mudanca = False

        for i in range(tamanho):
            for j in range(tamanho):
                celula = tabuleiro[i][j]

                # Processa apenas células numéricas já reveladas
                if isinstance(celula, int) and celula >= 0:
                    vizinhos = list(obter_vizinhos(i, j, tamanho))
                    ocultas = [(vx, vy) for vx, vy in vizinhos if tabuleiro[vx][vy] == -1]
                    minas_achadas = sum(1 for vx, vy in vizinhos if tabuleiro[vx][vy] == 'M')

                    # Dedução 1: todas as células desconhecidas vizinhas são minas
                    if celula - minas_achadas == len(ocultas) and len(ocultas) > 0:
                        for vx, vy in ocultas:
                            tabuleiro[vx][vy] = 'M'
                        houve_mudanca = True

                    # Dedução 2: todas as minas já foram marcadas, restante é seguro
                    elif minas_achadas == celula and len(ocultas) > 0:
                        for vx, vy in ocultas:
                            tabuleiro[vx][vy] = 'S'
                        houve_mudanca = True

    return tabuleiro


def exibir_tabuleiro(tabuleiro):
    """Imprime o tabuleiro com moldura e índices de linhas e colunas."""
    n = len(tabuleiro)
    header = "    " + " ".join(str(i) for i in range(n))
    divisoria = "   +" + "--" * n + "+"
    print(header)
    print(divisoria)
    for idx, linha in enumerate(tabuleiro):
        linha_formatada = " ".join(str(c) if c != -1 else "?" for c in linha)
        print(f" {idx} | {linha_formatada} |")
    print(divisoria)


if __name__ == "__main__":
    # Tabuleiro inicial de teste (9x9)
    # -1 representa célula oculta, números >= 0 são as dicas reveladas
    tabuleiro_inicial = [
        [1,  1,  1,  0, 0, 0, 0, 0, 0],
        [1, -1,  2,  1, 0, 0, 0, 0, 0],
        [1,  2, -1,  1, 0, 0, 0, 0, 0],
        [0,  1,  2,  2, 1, 0, 0, 0, 0],
        [0,  0,  1, -1, 1, 0, 0, 0, 0],
        [0,  0,  1,  1, 1, 0, 0, 0, 0],
        [0,  0,  0,  0, 0, 0, 0, 0, 0],
        [0,  0,  0,  0, 0, 0, 0, 0, 0],
        [0,  0,  0,  0, 0, 0, 0, 0, 0],
    ]

    print("=== Tabuleiro Inicial (com incógnitas '?') ===")
    exibir_tabuleiro(tabuleiro_inicial)

    resultado = resolver_campo_minado(tabuleiro_inicial)

    print("\n=== Tabuleiro Resolvido (M = Mina, S = Seguro) ===")
    exibir_tabuleiro(resultado)
