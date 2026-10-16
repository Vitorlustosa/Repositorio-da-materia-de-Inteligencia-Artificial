import random
import numpy as np
from collections import defaultdict
import time

# Parâmetros de reprodutibilidade e ambiente
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

EPISODIOS = 12000
BALAS_INTERVALO = (5, 8)  # Quantidade mínima e máxima de cartuchos por rodada
VIDA_INICIAL = 4
ITENS_POR_JOGADOR = 3

# Hiperparâmetros do Q-Learning
ALPHA = 0.1          # Taxa de aprendizado
GAMMA = 0.99         # Fator de desconto para recompensas futuras
EPS_INICIAL = 1.0    # Exploração máxima no início
EPS_FINAL = 0.05     # Exploração residual
EPS_DECAY = 0.99975  # Taxa de decaimento do epsilon

# Engenharia de Recompensas (Reward Shaping)
R_VITORIA = 10.0
R_DERROTA = -10.0
R_DANO_CAUSADO = 1.0
R_DANO_CANO_BONUS = 2.15
R_ALGEMA_OPORTUNA = 1.25
R_ITEM_DESPERDICADO = -1.8
R_PASSAR_TURNO = -0.2
R_TIRO_SI_REAL = -3.0     # Forte punição por atirar em si com bala real
R_TIRO_SI_FESTIM = 2.6    # Recompensa por atirar em si com festim (garante turno extra)


class BuckshotEnv:
    """
    Simulador do jogo Buckshot Roulette:
    - Espingarda calibre 12 carregada com cartuchos reais e de festim em ordem aleatória.
    - Dois itens utilizáveis:
        * 'cano': dobra o dano do próximo tiro se for bala real (+1 de dano).
        * 'algema': faz o oponente perder o próximo turno.
    - Atirar em si com festim mantém o turno do jogador.
    """

    def __init__(self, min_balas=5, max_balas=8, vida=VIDA_INICIAL, itens_iniciais=ITENS_POR_JOGADOR):
        self.min_balas = min_balas
        self.max_balas = max_balas
        self.vida_inicial = vida
        self.itens_iniciais = itens_iniciais
        self.reset()

    def reset(self):
        total = random.randint(self.min_balas, self.max_balas)
        reais = random.randint(1, max(1, total - 1))
        festim = total - reais

        # 1 = Real, 0 = Festim
        self.cartuchos = [1] * reais + [0] * festim
        random.shuffle(self.cartuchos)

        self.ponteiro = 0
        self.hp = {"player": self.vida_inicial, "bot": self.vida_inicial}

        itens_possiveis = ["cano", "algema"]
        self.itens = {
            "player": [random.choice(itens_possiveis) for _ in range(self.itens_iniciais)],
            "bot": [random.choice(itens_possiveis) for _ in range(self.itens_iniciais)]
        }

        self.cano_ativo = {"player": False, "bot": False}
        self.algemado = {"player": False, "bot": False}
        self.historico = []

        return self._obter_observacao()

    def _obter_observacao(self):
        restantes = self.cartuchos[self.ponteiro:]
        reais_restantes = sum(restantes)

        return {
            "reais_restantes": int(reais_restantes),
            "total_restantes": int(len(restantes)),
            "player_hp": int(self.hp["player"]),
            "bot_hp": int(self.hp["bot"]),
            "player_has_cano": int("cano" in self.itens["player"]),
            "player_has_algema": int("algema" in self.itens["player"]),
            "cano_ativo_player": int(self.cano_ativo["player"]),
            "bot_algemado": int(self.algemado["bot"]),
            "bot_has_cano": int("cano" in self.itens["bot"]),
            "bot_has_algema": int("algema" in self.itens["bot"])
        }

    def usar_item(self, autor, item):
        if item not in self.itens[autor]:
            return {"usou": False, "penalidade": R_ITEM_DESPERDICADO}

        self.itens[autor].remove(item)

        if item == "cano":
            self.cano_ativo[autor] = True
        elif item == "algema":
            oponente = "bot" if autor == "player" else "player"
            self.algemado[oponente] = True

        return {"usou": True, "penalidade": 0.0}

    def disparar(self, atirador, alvo):
        if self.ponteiro >= len(self.cartuchos):
            return 0, False

        bala = self.cartuchos[self.ponteiro]
        self.ponteiro += 1

        dano = 1 if bala == 1 else 0
        if self.cano_ativo[atirador]:
            if bala == 1:
                dano += 1
            self.cano_ativo[atirador] = False

        if dano > 0:
            self.hp[alvo] -= dano

        return dano, (bala == 1)

    def politica_bot(self):
        """Estratégia heurística com base na probabilidade de bala real."""
        restantes = self.cartuchos[self.ponteiro:]
        total = len(restantes)
        p_real = (sum(restantes) / total) if total > 0 else 0.5

        tem_cano = "cano" in self.itens["bot"]
        tem_algema = "algema" in self.itens["bot"]

        if tem_algema and self.hp["player"] > self.hp["bot"] and p_real > 0.4:
            return ("algema", "atirar_player")

        if tem_cano and p_real > 0.65:
            return ("cano", "atirar_player")

        if p_real >= 0.65:
            return ("none", "atirar_player")

        if p_real <= 0.20:
            return ("none", "atirar_self")

        return ("none", "atirar_player")

    def passo(self, acao):
        item_escolhido, tiro_escolhido = acao
        recompensa = 0.0

        # Incentivo para manter vantagem de vida
        dif_hp = self.hp["player"] - self.hp["bot"]
        recompensa += 0.1 * dif_hp

        # 1. Utiliza item selecionado
        if item_escolhido != "none":
            res_item = self.usar_item("player", item_escolhido)
            recompensa += res_item["penalidade"]

        # 2. Executa o disparo
        ganhou_turno_extra = False

        if tiro_escolhido == "enemy":
            dano, eh_real = self.disparar("player", "bot")
            if dano >= 2:
                recompensa += R_DANO_CANO_BONUS
            elif dano == 1:
                recompensa += R_DANO_CAUSADO

            if item_escolhido == "cano" and dano == 0:
                recompensa += R_ITEM_DESPERDICADO

        elif tiro_escolhido == "self":
            dano, eh_real = self.disparar("player", "player")
            if dano > 0:
                recompensa += R_TIRO_SI_REAL
            else:
                ganhou_turno_extra = True
                recompensa += R_TIRO_SI_FESTIM

            if item_escolhido == "cano" and dano == 0:
                recompensa += R_ITEM_DESPERDICADO

        elif tiro_escolhido == "none":
            if item_escolhido == "none" and self.ponteiro < len(self.cartuchos):
                recompensa += R_PASSAR_TURNO

        # Checa término imediato após a jogada do player
        finalizou = (self.hp["player"] <= 0 or self.hp["bot"] <= 0 or self.ponteiro >= len(self.cartuchos))
        if finalizou:
            if self.hp["player"] > self.hp["bot"]:
                recompensa += R_VITORIA
            elif self.hp["player"] < self.hp["bot"]:
                recompensa += R_DERROTA
            return self._obter_observacao(), recompensa, True

        # Se acertou festim em si mesmo, retém a vez
        if ganhou_turno_extra:
            return self._obter_observacao(), recompensa, False

        # 3. Turno do Bot
        if self.algemado["bot"]:
            restantes = self.cartuchos[self.ponteiro:]
            if restantes and (sum(restantes) / len(restantes)) > 0.5:
                recompensa += R_ALGEMA_OPORTUNA
            self.algemado["bot"] = False
        else:
            turnos_bot = 0
            while turnos_bot < 2:
                turnos_bot += 1
                bot_item, bot_tiro = self.politica_bot()

                if bot_item != "none":
                    self.usar_item("bot", bot_item)

                if bot_tiro == "atirar_player":
                    dano_b, _ = self.disparar("bot", "player")
                    if dano_b > 0:
                        recompensa -= R_DANO_CAUSADO * dano_b
                    break

                elif bot_tiro == "atirar_self":
                    dano_b, _ = self.disparar("bot", "bot")
                    if dano_b > 0:
                        recompensa += 0.5 * dano_b
                        break
                    else:
                        # Bot deu festim em si mesmo e joga novamente
                        continue

        # Checa término após ação do Bot
        finalizou = (self.hp["player"] <= 0 or self.hp["bot"] <= 0 or self.ponteiro >= len(self.cartuchos))
        if finalizou:
            if self.hp["player"] > self.hp["bot"]:
                recompensa += R_VITORIA
            elif self.hp["player"] < self.hp["bot"]:
                recompensa += R_DERROTA
            return self._obter_observacao(), recompensa, True

        return self._obter_observacao(), recompensa, False


# Espaço discreto de ações combinadas
ITENS = ["none", "cano", "algema"]
TIROS = ["enemy", "self", "none"]
ACOES = [(it, tr) for it in ITENS for tr in TIROS]


class AgenteQLearning:
    """Agente de Aprendizado por Reforço com Q-Table e Action Masking."""

    def __init__(self, acoes=ACOES):
        self.acoes = acoes
        self.q = defaultdict(float)
        self.alpha = ALPHA
        self.gamma = GAMMA
        self.eps = EPS_INICIAL

    def serializar_estado(self, obs):
        return (
            obs["reais_restantes"],
            obs["total_restantes"],
            obs["player_hp"],
            obs["bot_hp"],
            obs["player_has_cano"],
            obs["player_has_algema"],
            obs["cano_ativo_player"],
            obs["bot_algemado"]
        )

    def acoes_validas(self, obs):
        """Mascara de ações legais (Action Masking) para acelerar a convergência."""
        indices_validos = []
        tem_cano = obs["player_has_cano"] == 1
        tem_algema = obs["player_has_algema"] == 1
        cano_ativo = obs["cano_ativo_player"] == 1

        for idx, (item, tiro) in enumerate(self.acoes):
            valido = True
            if item == "cano" and not tem_cano and not cano_ativo:
                valido = False
            elif item == "algema" and not tem_algema:
                valido = False

            if tiro != "none" and obs["total_restantes"] == 0:
                valido = False

            if valido:
                indices_validos.append(idx)

        return indices_validos if indices_validos else [0]

    def escolher_acao(self, obs, em_avaliacao=False):
        validas = self.acoes_validas(obs)

        # Política Epsilon-Greedy
        if not em_avaliacao and random.random() < self.eps:
            return random.choice(validas)

        # Explotação: seleciona a ação com maior valor Q previsto
        s = self.serializar_estado(obs)
        melhor_q = -float('inf')
        melhor_a = validas[0]

        for a_idx in validas:
            q_val = self.q[(s, a_idx)]
            if q_val > melhor_q:
                melhor_q = q_val
                melhor_a = a_idx

        return melhor_a

    def atualizar(self, obs, a_idx, recompensa, prox_obs, finalizou):
        s = self.serializar_estado(obs)
        q_atual = self.q[(s, a_idx)]

        if finalizou:
            q_alvo = recompensa
        else:
            s_prox = self.serializar_estado(prox_obs)
            validas_prox = self.acoes_validas(prox_obs)
            max_prox = max(self.q[(s_prox, a)] for a in validas_prox) if validas_prox else 0.0
            q_alvo = recompensa + self.gamma * max_prox

        # Equação de Bellman
        self.q[(s, a_idx)] += self.alpha * (q_alvo - q_atual)

    def decair_epsilon(self):
        self.eps = max(EPS_FINAL, self.eps * EPS_DECAY)


def treinar():
    env = BuckshotEnv()
    agente = AgenteQLearning()

    janela = 1000
    vitorias_janela = 0
    t_inicio = time.time()

    print("=" * 65)
    print(f"  Treinando Q-Learning no Buckshot Roulette ({EPISODIOS} episódios)")
    print("=" * 65)

    for ep in range(1, EPISODIOS + 1):
        obs = env.reset()

        while True:
            a_idx = agente.escolher_acao(obs)
            acao = ACOES[a_idx]

            prox_obs, recompensa, finalizou = env.passo(acao)
            agente.atualizar(obs, a_idx, recompensa, prox_obs, finalizou)

            obs = prox_obs

            if finalizou:
                if env.hp["player"] > env.hp["bot"]:
                    vitorias_janela += 1
                break

        agente.decair_epsilon()

        if ep % janela == 0:
            taxa_win = (vitorias_janela / janela) * 100
            decorrido = time.time() - t_inicio
            print(f"  Episódio {ep:5d}/{EPISODIOS} | Win Rate: {taxa_win:5.1f}% | Epsilon: {agente.eps:.3f} | Tempo: {decorrido:.1f}s")
            vitorias_janela = 0

    return agente


def avaliar(agente, num_jogos=500):
    env = BuckshotEnv()
    vitorias, derrotas, empates = 0, 0, 0

    for _ in range(num_jogos):
        obs = env.reset()
        while True:
            a_idx = agente.escolher_acao(obs, em_avaliacao=True)
            acao = ACOES[a_idx]
            obs, _, finalizou = env.passo(acao)

            if finalizou:
                if env.hp["player"] > env.hp["bot"]:
                    vitorias += 1
                elif env.hp["player"] < env.hp["bot"]:
                    derrotas += 1
                else:
                    empates += 1
                break

    return vitorias, derrotas, empates


if __name__ == "__main__":
    agente_treinado = treinar()

    print("\n" + "=" * 50)
    print("       AVALIAÇÃO FINAL DA POLÍTICA ÓTIMA")
    print("=" * 50)
    vitorias, derrotas, empates = avaliar(agente_treinado, num_jogos=500)
    total = vitorias + derrotas + empates

    print(f"• Partidas Avaliadas : {total}")
    print(f"• Vitórias do Agente : {vitorias} ({vitorias/total*100:.1f}%)")
    print(f"• Derrotas          : {derrotas} ({derrotas/total*100:.1f}%)")
    print(f"• Empates           : {empates} ({empates/total*100:.1f}%)")
    print("=" * 50)
