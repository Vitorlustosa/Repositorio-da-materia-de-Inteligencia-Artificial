def exibir_tabuleiro(tabuleiro):
    """Exibe o tabuleiro de Sudoku formatado com divisórias de blocos 3x3."""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)

        linha_str = []
        for j in range(9):
            if j % 3 == 0 and j != 0:
                linha_str.append("|")
            val = tabuleiro[i][j]
            linha_str.append(str(val) if val != 0 else ".")

        print(" ".join(linha_str))


def proxima_celula_vazia(tabuleiro):
    """Localiza a primeira célula vazia (valor 0). Retorna (linha, coluna) ou None se cheio."""
    for i in range(9):
        for j in range(9):
            if tabuleiro[i][j] == 0:
                return (i, j)
    return None


def jogada_valida(tabuleiro, numero, pos):
    """
    Verifica se colocar 'numero' em pos=(linha, col) viola alguma regra do Sudoku:
    - Sem duplicatas na mesma linha
    - Sem duplicatas na mesma coluna
    - Sem duplicatas no mesmo quadrante 3x3
    """
    linha, col = pos

    # Verifica linha
    if any(tabuleiro[linha][j] == numero for j in range(9) if j != col):
        return False

    # Verifica coluna
    if any(tabuleiro[i][col] == numero for i in range(9) if i != linha):
        return False

    # Verifica bloco 3x3
    bloco_r = (linha // 3) * 3
    bloco_c = (col // 3) * 3
    for r in range(bloco_r, bloco_r + 3):
        for c in range(bloco_c, bloco_c + 3):
            if tabuleiro[r][c] == numero and (r, c) != pos:
                return False

    return True


def resolver_sudoku(tabuleiro):
    """
    Resolve o tabuleiro usando busca com retrocesso (Backtracking).
    Testa valores de 1 a 9 recursivamente. Ao encontrar um beco sem saída,
    desfaz a atribuição (reset para 0) e tenta o próximo candidato.
    """
    vazia = proxima_celula_vazia(tabuleiro)
    if not vazia:
        return True  # Todas as células foram preenchidas

    linha, col = vazia

    for num in range(1, 10):
        if jogada_valida(tabuleiro, num, (linha, col)):
            tabuleiro[linha][col] = num

            # Continua recursivamente para as próximas células
            if resolver_sudoku(tabuleiro):
                return True

            # Se nenhum número subsequente levou à solução, desfaz a jogada
            tabuleiro[linha][col] = 0

    return False


if __name__ == "__main__":
    # Tabuleiro de teste clássico (0 = célula a ser descoberta)
    tabuleiro_teste = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    print("=== Tabuleiro Inicial ===")
    exibir_tabuleiro(tabuleiro_teste)

    print("\nResolvendo com Backtracking...\n")
    if resolver_sudoku(tabuleiro_teste):
        print("=== Solução Encontrada ===")
        exibir_tabuleiro(tabuleiro_teste)
    else:
        print("Não foi encontrada solução válida para a configuração informada.")