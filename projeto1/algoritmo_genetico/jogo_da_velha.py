import random

class JogoDaVelha:
    """Ambiente do jogo da velha com tabuleiro 3x3 indexado de 0 a 8."""

    LINHAS_VITORIA = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontais
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Verticais
        [0, 4, 8], [2, 4, 6]              # Diagonais
    ]

    def __init__(self):
        self.tabuleiro = [' '] * 9

    def movimentos_disponiveis(self):
        return [i for i, casa in enumerate(self.tabuleiro) if casa == ' ']

    def realizar_jogada(self, posicao, simbolo):
        if self.tabuleiro[posicao] == ' ':
            self.tabuleiro[posicao] = simbolo
            return True
        return False

    def checar_vitoria(self, simbolo):
        for linha in self.LINHAS_VITORIA:
            if all(self.tabuleiro[idx] == simbolo for idx in linha):
                return True
        return False

    def deu_empate(self):
        return ' ' not in self.tabuleiro

    def resetar(self):
        self.tabuleiro = [' '] * 9


class AgenteGenetico:
    """
    Agente evolucionário cujo cromossomo é uma tabela de política (estratégia):
    mapeia cada configuração de tabuleiro para o índice da jogada (0 a 8).
    """

    def __init__(self, estrategia=None):
        self.estrategia = estrategia if estrategia is not None else {}
        self.aptidao = 0

    def escolher_jogada(self, estado_tabuleiro, jogadas_validas):
        estado_tupla = tuple(estado_tabuleiro)

        # Se já possui resposta mapeada e o movimento é legal, executa
        if estado_tupla in self.estrategia and self.estrategia[estado_tupla] in jogadas_validas:
            return self.estrategia[estado_tupla]

        # Caso contrário, descobre nova ação e armazena na memória
        jogada = random.choice(jogadas_validas)
        self.estrategia[estado_tupla] = jogada
        return jogada


def simular_partida_treino(jogador1, jogador2, simb1='X', simb2='O'):
    """Simula uma partida e pontua a aptidão (fitness) dos agentes."""
    jogo = JogoDaVelha()
    jog_atual, jog_outro = jogador1, jogador2
    simb_atual, simb_outro = simb1, simb2

    while True:
        validas = jogo.movimentos_disponiveis()
        if not validas:
            # Empate: recompensa moderada
            jog_atual.aptidao += 1
            jog_outro.aptidao += 1
            break

        movimento = jog_atual.escolher_jogada(jogo.tabuleiro, validas)

        if movimento not in validas:
            # Penalidade drástica por tentativa inválida
            jog_atual.aptidao -= 20
            jog_outro.aptidao += 10
            break

        jogo.realizar_jogada(movimento, simb_atual)

        if jogo.checar_vitoria(simb_atual):
            jog_atual.aptidao += 10
            jog_outro.aptidao -= 5
            break

        jog_atual, jog_outro = jog_outro, jog_atual
        simb_atual, simb_outro = simb_outro, simb_atual


def avaliar_populacao(populacao):
    """Realiza round-robin em que cada agente enfrenta os demais como 'X' e como 'O'."""
    for agente in populacao:
        agente.aptidao = 0

    n = len(populacao)
    for i in range(n):
        for j in range(i + 1, n):
            simular_partida_treino(populacao[i], populacao[j], 'X', 'O')
            simular_partida_treino(populacao[j], populacao[i], 'X', 'O')


def recombinacao(pai1, pai2):
    """Crossover: combina os genes (regras de jogada) de ambos os pais."""
    filho_estrategia = {}
    todas_chaves = set(pai1.estrategia.keys()) | set(pai2.estrategia.keys())

    for chave in todas_chaves:
        if random.random() < 0.5:
            if chave in pai1.estrategia:
                filho_estrategia[chave] = pai1.estrategia[chave]
        else:
            if chave in pai2.estrategia:
                filho_estrategia[chave] = pai2.estrategia[chave]

    return AgenteGenetico(estrategia=filho_estrategia)


def mutacao(agente, taxa_mutacao):
    """Aplica mutação aleatória removendo genes para forçar exploração de novas jogadas."""
    if not agente.estrategia or taxa_mutacao <= 0:
        return agente

    quantidade = max(1, int(len(agente.estrategia) * taxa_mutacao))
    chaves_sorteadas = random.sample(list(agente.estrategia.keys()), min(quantidade, len(agente.estrategia)))

    for chave in chaves_sorteadas:
        del agente.estrategia[chave]

    return agente


def treinar_agente_genetico(geracoes, tam_populacao, num_pais, taxa_mutacao):
    populacao = [AgenteGenetico() for _ in range(tam_populacao)]

    for gen in range(geracoes):
        avaliar_populacao(populacao)
        populacao.sort(key=lambda a: a.aptidao, reverse=True)
        melhor_aptidao = populacao[0].aptidao

        if (gen + 1) % max(1, geracoes // 5) == 0 or gen == geracoes - 1:
            print(f"  Geração {gen + 1:3d}/{geracoes} | Melhor Aptidão: {melhor_aptidao}")

        pais = populacao[:num_pais]
        nova_populacao = [AgenteGenetico(estrategia=dict(p.estrategia)) for p in pais]

        while len(nova_populacao) < tam_populacao:
            p1, p2 = random.sample(pais, 2)
            filho = recombinacao(p1, p2)
            filho = mutacao(filho, taxa_mutacao)
            nova_populacao.append(filho)

        populacao = nova_populacao

    avaliar_populacao(populacao)
    populacao.sort(key=lambda a: a.aptidao, reverse=True)
    return populacao[0]


class AgenteMinimax:
    """
    Agente ótimo baseado no algoritmo Minimax.
    Possui uma probabilidade controlada de cometer falhas para simular jogador humano/falível.
    """

    def __init__(self, chance_erro=0.1):
        self.chance_erro = chance_erro
        self.simbolo = 'O'
        self.oponente = 'X'

    def definir_simbolos(self, meu_simbolo):
        self.simbolo = meu_simbolo
        self.oponente = 'O' if meu_simbolo == 'X' else 'X'

    def escolher_jogada(self, tabuleiro, jogadas_validas):
        # Sorteia erro estocástico para não ser 100% perfeito
        if random.random() < self.chance_erro:
            return random.choice(jogadas_validas)

        jogo_simulado = JogoDaVelha()
        jogo_simulado.tabuleiro = list(tabuleiro)
        resultado = self._minimax(jogo_simulado, self.simbolo)
        return resultado['movimento']

    def _minimax(self, estado_jogo, jogador_atual):
        outro = 'O' if jogador_atual == 'X' else 'X'

        if estado_jogo.checar_vitoria(outro):
            return {'score': -1}
        if estado_jogo.deu_empate():
            return {'score': 0}

        melhores_movimentos = []
        for mov in estado_jogo.movimentos_disponiveis():
            estado_jogo.realizar_jogada(mov, jogador_atual)
            retorno = self._minimax(estado_jogo, outro)
            estado_jogo.tabuleiro[mov] = ' '  # Desfaz para testar alternativas

            score_invertido = -retorno['score']
            melhores_movimentos.append({'movimento': mov, 'score': score_invertido})

        if jogador_atual == self.simbolo:
            return max(melhores_movimentos, key=lambda x: x['score'])
        else:
            return min(melhores_movimentos, key=lambda x: x['score'])


def simular_duelo(agente1, agente2, simb1='X', simb2='O'):
    """Executa 1 partida sem alterar fitness. Retorna 'X', 'O' ou 'Empate'."""
    jogo = JogoDaVelha()

    if isinstance(agente1, AgenteMinimax):
        agente1.definir_simbolos(simb1)
    if isinstance(agente2, AgenteMinimax):
        agente2.definir_simbolos(simb2)

    jog_atual, jog_outro = agente1, agente2
    simb_atual, simb_outro = simb1, simb2

    while True:
        validas = jogo.movimentos_disponiveis()
        if not validas:
            return "Empate"

        mov = jog_atual.escolher_jogada(jogo.tabuleiro, validas)
        if mov not in validas:
            return simb_outro  # Derrota por jogada ilegal

        jogo.realizar_jogada(mov, simb_atual)

        if jogo.checar_vitoria(simb_atual):
            return simb_atual

        jog_atual, jog_outro = jog_outro, jog_atual
        simb_atual, simb_outro = simb_outro, simb_atual


def executar_torneio():
    print("=" * 60)
    print("   Torneio IA: Algoritmo Genético vs Minimax (Jogo da Velha)")
    print("=" * 60)

    def ler_int(msg, default):
        try:
            val = input(f"{msg} [padrão: {default}]: ").strip()
            return int(val) if val else default
        except (ValueError, EOFError, KeyboardInterrupt):
            print()
            return default

    def ler_float(msg, default):
        try:
            val = input(f"{msg} [padrão: {default}]: ").strip()
            return float(val) if val else default
        except (ValueError, EOFError, KeyboardInterrupt):
            print()
            return default

    geracoes = ler_int("Número de gerações", 50)
    tam_pop = ler_int("Tamanho da população", 40)
    num_pais = ler_int("Número de reprodutores (pais)", 10)
    taxa_mut = ler_float("Taxa de mutação (ex: 0.03)", 0.03)

    print("\nIniciando evolução do Agente Genético...")
    melhor_ga = treinar_agente_genetico(geracoes, tam_pop, num_pais, taxa_mut)
    print("Evolução concluída! Agente treinado com sucesso.\n")

    partidas = ler_int("Partidas para o torneio final", 100)
    taxa_erro_minimax = ler_float("Chance de erro do Minimax (0.0 a 1.0)", 0.15)

    agente_minimax = AgenteMinimax(chance_erro=taxa_erro_minimax)

    placar = {"GA": 0, "Minimax": 0, "Empates": 0}
    metade = partidas // 2

    # Rodada 1: GA joga de X (primeiro a jogar)
    for _ in range(metade):
        venc = simular_duelo(melhor_ga, agente_minimax, 'X', 'O')
        if venc == 'X':
            placar["GA"] += 1
        elif venc == 'O':
            placar["Minimax"] += 1
        else:
            placar["Empates"] += 1

    # Rodada 2: Minimax joga de X
    for _ in range(partidas - metade):
        venc = simular_duelo(agente_minimax, melhor_ga, 'X', 'O')
        if venc == 'X':
            placar["Minimax"] += 1
        elif venc == 'O':
            placar["GA"] += 1
        else:
            placar["Empates"] += 1

    print("\n" + "=" * 45)
    print("           RESULTADO FINAL DO TORNEIO")
    print("=" * 45)
    print(f"Total de Partidas : {partidas}")
    print(f"Vitórias GA       : {placar['GA']} ({placar['GA']/partidas*100:.1f}%)")
    print(f"Vitórias Minimax  : {placar['Minimax']} ({placar['Minimax']/partidas*100:.1f}%)")
    print(f"Empates           : {placar['Empates']} ({placar['Empates']/partidas*100:.1f}%)")
    print("=" * 45)


if __name__ == "__main__":
    executar_torneio()