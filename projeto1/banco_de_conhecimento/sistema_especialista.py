def recomendar_treino(dados_usuario):
    """
    Sistema especialista baseado em regras de produção:
    - Base de fatos: perfil do praticante (objetivo, nível, frequência, restrição)
    - Motor de inferência: avalia as condições e infere a melhor prescrição de treino
    """
    objetivo = dados_usuario.get("objetivo", "hipertrofia").lower()
    nivel = dados_usuario.get("nivel", "iniciante").lower()
    dias = dados_usuario.get("dias_semana", 3)
    restricao = dados_usuario.get("restricao")

    prescricao = {}

    # 1. Regra para divisão e volume conforme objetivo e nível
    if objetivo == "hipertrofia":
        if nivel == "iniciante":
            prescricao["tipo"] = "Divisão AB (Superior / Inferior)"
            prescricao["descricao"] = "Foco na adaptação neural e máquinas guiadas (3 séries de 10 a 12 repetições)."
        elif nivel == "intermediario":
            prescricao["tipo"] = "Divisão ABC (Push / Pull / Legs)"
            prescricao["descricao"] = "Volume moderado a alto (4 séries de 8 a 10) com progressão linear de carga."
        elif nivel == "avancado":
            prescricao["tipo"] = "Divisão ABCDEF (Grupos isolados)"
            prescricao["descricao"] = "Alta intensidade com técnicas avançadas (drop-sets, rest-pause) para grupos específicos."
        else:
            prescricao["tipo"] = "Personalizado"
            prescricao["descricao"] = "Nível de experiência não identificado, sugerido iniciar com adaptação anatômica."

    elif objetivo == "resistencia":
        prescricao["tipo"] = "Treino em Circuito Funcional"
        prescricao["descricao"] = "Alta densidade, intervalos curtos de descanso (30-45s) e séries de 15 a 20 repetições."

    elif objetivo in ["perda de peso", "emagrecimento"]:
        prescricao["tipo"] = "Fullbody Integrado com HIIT"
        prescricao["descricao"] = "Exercícios multiarticulares conjugados com cardio intervalado para maximizar o gasto calórico."

    else:
        prescricao["tipo"] = "Indefinido"
        prescricao["descricao"] = "Objetivo não cadastrado na base de regras."

    # 2. Regra de ajuste pela frequência semanal
    if dias < 3:
        prescricao["ajuste_frequencia"] = "Como a disponibilidade é menor que 3 dias, adote fullbody para estimular o corpo todo por sessão."
    elif dias >= 5:
        prescricao["ajuste_frequencia"] = "Com 5 ou mais dias disponíveis, distribua em divisões isoladas (ex: costas/bíceps, peito/tríceps) para garantir recuperação."
    else:
        prescricao["ajuste_frequencia"] = "Frequência de 3 a 4 dias é ideal para divisões no formato ABC ou Upper/Lower."

    # 3. Regra de adaptação por limitações ortopédicas
    if restricao == "ombro":
        prescricao["cuidados"] = "Atenção: Evite desenvolvimentos atrás da nuca e supinos retos com barra; priorize halteres e polias com pegada neutra."
    elif restricao == "joelho":
        prescricao["cuidados"] = "Atenção: Evite agachamento profundo livre; utilize leg press 45° com amplitude controlada e fortaleça posteriores."
    elif restricao == "costas":
        prescricao["cuidados"] = "Atenção: Evite levantamento terra e remadas curvadas livres; utilize apoios no peito e remadas articuladas."
    else:
        prescricao["cuidados"] = "Nenhuma restrição articular reportada. Mantenha boa técnica de execução."

    return prescricao


def coletar_dados():
    """Interface interativa para montagem da base de fatos."""
    print("=== Sistema Especialista: Prescrição Inteligente de Treino ===")
    print("Responda às perguntas abaixo (pressione Enter para usar o valor padrão).\n")

    def ler_campo(msg, padrao):
        try:
            val = input(f"{msg} [padrão: {padrao}]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return padrao
        return val.lower() if val else padrao

    nivel = ler_campo("1. Seu nível de experiência (iniciante / intermediario / avancado)", "iniciante")
    objetivo = ler_campo("2. Seu objetivo principal (hipertrofia / resistencia / perda de peso)", "hipertrofia")

    while True:
        dias_str = ler_campo("3. Quantos dias na semana você treina? (1 a 7)", "4")
        try:
            dias = int(dias_str)
            if 1 <= dias <= 7:
                break
            print("Digite um valor entre 1 e 7.")
        except ValueError:
            print("Por favor, digite um número inteiro.")

    restricao = ler_campo("4. Alguma restrição/lesão? (ombro / joelho / costas / nenhuma)", "nenhuma")
    if restricao == "nenhuma":
        restricao = None

    return {
        "nivel": nivel,
        "objetivo": objetivo,
        "dias_semana": dias,
        "restricao": restricao
    }


if __name__ == "__main__":
    usuario = coletar_dados()
    recomendacao = recomendar_treino(usuario)

    print("\n" + "=" * 50)
    print("        RELATÓRIO DE PRESCRIÇÃO DE TREINO")
    print("=" * 50)
    print(f"• Estrutura Recomendada : {recomendacao['tipo']}")
    print(f"• Metodologia           : {recomendacao['descricao']}")
    print(f"• Ajuste de Rotina      : {recomendacao['ajuste_frequencia']}")
    print(f"• Segurança e Cuidados  : {recomendacao['cuidados']}")
    print("=" * 50)