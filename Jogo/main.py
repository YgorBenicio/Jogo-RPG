import json
import os
from random import choice, choices, randint

from dados import (
    ARMAS, BAU_TIERS, CLASSES, EFEITOS, FASES, LOJA,
    PRECO_POCAO_MANA, PRECO_POCAO_VIDA, TIERS,
)

PASTA_SAVES = "saves"
ETAPAS = ["mob", "boss"]
CHANCE_ERRO = 10
CHANCE_CRITICO = 10
CUSTO_ESPECIAL = 10


def sortear(chance):
    return randint(1, 100) <= chance


def criar_jogador(nome, classe):
    return {
        "nome": nome,
        "classe": classe["nome"],
        "level": 1,
        "exp": 0,
        "exp_max": 20,
        "vida": classe["vida"],
        "vida_max": classe["vida"],
        "mana": classe["mana"],
        "mana_max": classe["mana"],
        "dano": classe["dano"],
        "pocoes_vida": 2,
        "pocoes_mana": 1,
        "ouro": 0,
        "fase": 1,
        "efeito": None,
        "equipamentos": {},
        "stats": {"niveis": 0, "pocoes_usadas": 0, "turnos": 0},
    }


def criar_monstro(modelo):
    monstro = dict(modelo)
    monstro["vida_max"] = modelo["vida"]
    return monstro


def bonus_equipamento(jogador, tipo):
    item = jogador["equipamentos"].get(tipo)
    return item["nivel"] if item else 0


def descrever(item):
    return f"{item['nome']} (Tier {item['tier']}, nível {item['nivel']})"


def em_andamento(jogador, monstro):
    return jogador["vida"] > 0 and monstro["vida"] > 0


def exibir_status(jogador, monstro):
    especial = monstro["especial"]
    efeito = jogador["efeito"]
    print("\n" + "-" * 60)
    print(f"{jogador['nome']} ({jogador['classe']}) | Level {jogador['level']} | "
          f"Exp {jogador['exp']}/{jogador['exp_max']}")
    print(f"Vida {jogador['vida']}/{jogador['vida_max']} | "
          f"Mana {jogador['mana']}/{jogador['mana_max']} | Dano {jogador['dano']}")
    print(f"Poções: vida {jogador['pocoes_vida']}, mana {jogador['pocoes_mana']}")
    if efeito:
        print(f"Efeito: {EFEITOS[efeito['id']]['nome']} ({efeito['turnos']} turnos)")
    print(f"{monstro['nome']}: Vida {monstro['vida']}/{monstro['vida_max']} | "
          f"Dano máx. {monstro['dano']}")
    print(f"Especial: {especial['nome']} ({especial['chance']}%)")


def subir_de_nivel(jogador):
    while jogador["exp"] >= jogador["exp_max"]:
        jogador["exp"] -= jogador["exp_max"]
        jogador["level"] += 1
        jogador["exp_max"] = int(jogador["exp_max"] * 1.5)
        jogador["vida_max"] += 20
        jogador["mana_max"] += 5
        jogador["dano"] += 4
        jogador["stats"]["niveis"] += 1
        print(f"Subiu para o level {jogador['level']}!")


def turno_do_jogador(jogador, monstro):
    print("\n[1] Atacar  [2] Especial (10 de mana)  [3] Defender")
    print(f"[4] Poção de vida  [5] Poção de mana  [6] Salvar e sair")
    escolha = input("Ação: ")

    if escolha == "1":
        if sortear(CHANCE_ERRO):
            print("Você errou o ataque.")
            return "ok"
        dano = randint(jogador["dano"] // 2, jogador["dano"])
        dano += bonus_equipamento(jogador, "Espada") // 2
        if sortear(CHANCE_CRITICO + bonus_equipamento(jogador, "Arco") // 2):
            dano *= 2
            print("Acerto crítico!")
        monstro["vida"] -= dano
        print(f"Você causou {dano} de dano.")
    elif escolha == "2":
        if jogador["mana"] < CUSTO_ESPECIAL:
            print("Mana insuficiente.")
            return "invalido"
        jogador["mana"] -= CUSTO_ESPECIAL
        dano = randint(jogador["dano"], jogador["dano"] * 2)
        dano += bonus_equipamento(jogador, "Cajado")
        monstro["vida"] -= dano
        print(f"Ataque especial! Você causou {dano} de dano.")
    elif escolha == "3":
        print("Você se prepara para o próximo golpe.")
        return "defesa"
    elif escolha == "4":
        if jogador["pocoes_vida"] == 0:
            print("Você não tem poções de vida.")
            return "invalido"
        jogador["pocoes_vida"] -= 1
        jogador["stats"]["pocoes_usadas"] += 1
        jogador["vida"] = min(jogador["vida_max"], jogador["vida"] + 50)
        print("Você recuperou vida.")
    elif escolha == "5":
        if jogador["pocoes_mana"] == 0:
            print("Você não tem poções de mana.")
            return "invalido"
        jogador["pocoes_mana"] -= 1
        jogador["stats"]["pocoes_usadas"] += 1
        jogador["mana"] = min(jogador["mana_max"], jogador["mana"] + 30)
        print("Você recuperou mana.")
    elif escolha == "6":
        return "sair"
    else:
        print("Opção inválida.")
        return "invalido"
    return "ok"


def turno_do_monstro(jogador, monstro, defendendo):
    if sortear(CHANCE_ERRO):
        print(f"{monstro['nome']} errou o ataque.")
        return

    especial = monstro["especial"]
    usou_especial = sortear(especial["chance"])
    dano = randint(monstro["dano"] // 2, monstro["dano"])
    if usou_especial:
        dano = int(dano * especial["multiplicador"])
        print(f"{monstro['nome']} usou {especial['nome']}!")

    dano -= bonus_equipamento(jogador, "Escudo") // 3
    if defendendo:
        dano //= 2
    dano = max(1, dano)
    jogador["vida"] -= dano
    print(f"{monstro['nome']} causou {dano} de dano.")

    if usou_especial and sortear(especial["chance_efeito"]):
        efeito = EFEITOS[especial["efeito"]]
        jogador["efeito"] = {"id": especial["efeito"], "turnos": efeito["turnos"]}
        print(f"Você está com {efeito['nome']}!")


def aplicar_efeito(jogador):
    efeito = jogador["efeito"]
    if not efeito:
        return
    dados = EFEITOS[efeito["id"]]
    jogador["vida"] -= dados["dano"]
    efeito["turnos"] -= 1
    print(f"{dados['nome']} causou {dados['dano']} de dano em você.")
    if efeito["turnos"] == 0:
        jogador["efeito"] = None
        print(f"{dados['nome']} passou.")


def aplicar_evento(evento, jogador, monstro):
    if not sortear(evento["chance"]):
        return
    dano = randint(evento["dano"] // 2, evento["dano"])
    if choice(["jogador", "monstro"]) == "jogador":
        jogador["vida"] -= dano
        alvo = "você"
    else:
        monstro["vida"] -= dano
        alvo = monstro["nome"]
    print(f"{evento['nome']} e atinge {alvo}: {dano} de dano.")


def batalhar(jogador, monstro, numero, etapa):
    evento = FASES[numero]["evento"]
    print(f"\n===== {jogador['nome']} vs {monstro['nome']} =====")

    while em_andamento(jogador, monstro):
        exibir_status(jogador, monstro)
        resultado = turno_do_jogador(jogador, monstro)

        if resultado == "invalido":
            continue
        if resultado == "sair":
            salvar_jogo(jogador, {"fase": numero, "etapa": etapa, "monstro": monstro})
            print("Jogo salvo.")
            return "salvou"

        jogador["stats"]["turnos"] += 1
        if em_andamento(jogador, monstro):
            turno_do_monstro(jogador, monstro, resultado == "defesa")
        if em_andamento(jogador, monstro):
            aplicar_efeito(jogador)
        if em_andamento(jogador, monstro):
            aplicar_evento(evento, jogador, monstro)

    return "vitoria" if jogador["vida"] > 0 else "derrota"


def receber_recompensa(jogador, monstro):
    jogador["exp"] += monstro["exp"]
    jogador["ouro"] += monstro["ouro"]
    jogador["pocoes_vida"] += 1
    print(f"\nVitória! +{monstro['exp']} de experiência, +{monstro['ouro']} de ouro "
          f"e 1 poção de vida.")
    subir_de_nivel(jogador)


def oferecer_item(jogador, item):
    atual = jogador["equipamentos"].get(item["tipo"])
    if atual:
        print(f"Equipado atualmente: {descrever(atual)}")
        if input("Trocar pelo novo item? (s/n): ").lower() != "s":
            return False
    jogador["equipamentos"][item["tipo"]] = item
    print(f"Equipado: {descrever(item)}")
    return True


def abrir_bau(jogador, numero):
    fase = FASES[numero]
    tier = choices([1, 2, 3], weights=BAU_TIERS[numero])[0]
    tipo = choice(list(ARMAS))
    minimo, maximo = TIERS[tier]
    item = {
        "nome": f"{tipo} {fase['sufixo']}",
        "tipo": tipo,
        "tier": tier,
        "nivel": randint(minimo, maximo),
    }
    print(f"\nO chefe deixou um baú! Você encontrou: {descrever(item)}")
    print(f"Efeito: {ARMAS[tipo]}")
    oferecer_item(jogador, item)


def loja(jogador, numero):
    armas = LOJA[numero]
    while True:
        print(f"\n===== Loja | Ouro: {jogador['ouro']} =====")
        print(f"[1] Poção de vida - {PRECO_POCAO_VIDA} de ouro")
        print(f"[2] Poção de mana - {PRECO_POCAO_MANA} de ouro")
        for posicao, item in enumerate(armas, start=3):
            print(f"[{posicao}] {descrever(item)} - {item['preco']} de ouro | {ARMAS[item['tipo']]}")
        print("[0] Sair da loja")
        escolha = input("Comprar: ")

        if escolha == "0":
            return
        if escolha == "1" or escolha == "2":
            preco = PRECO_POCAO_VIDA if escolha == "1" else PRECO_POCAO_MANA
            if jogador["ouro"] < preco:
                print("Ouro insuficiente.")
                continue
            jogador["ouro"] -= preco
            jogador["pocoes_vida" if escolha == "1" else "pocoes_mana"] += 1
            print("Poção comprada.")
        elif escolha.isdigit() and 3 <= int(escolha) < 3 + len(armas):
            item = armas[int(escolha) - 3]
            if jogador["ouro"] < item["preco"]:
                print("Ouro insuficiente.")
                continue
            if oferecer_item(jogador, dict(item)):
                jogador["ouro"] -= item["preco"]
        else:
            print("Opção inválida.")


def restaurar(jogador):
    jogador["vida"] = jogador["vida_max"]
    jogador["mana"] = jogador["mana_max"]
    jogador["efeito"] = None


def jogar_fase(jogador, numero, etapa_inicial="mob", monstro=None):
    fase = FASES[numero]
    print(f"\n########## Fase {numero}: {fase['nome']} ##########")

    for etapa in ETAPAS[ETAPAS.index(etapa_inicial):]:
        if monstro is None:
            monstro = criar_monstro(fase[etapa])

        resultado = batalhar(jogador, monstro, numero, etapa)
        if resultado == "salvou":
            return "salvou"

        restaurar(jogador)
        if resultado == "derrota":
            print("\nVocê foi derrotado. Volte mais forte.")
            return "derrota"

        receber_recompensa(jogador, monstro)
        if etapa == "boss":
            abrir_bau(jogador, numero)
        loja(jogador, numero)
        salvar_jogo(jogador, None)
        monstro = None

    return "vitoria"


def processar_fase(jogador, numero, etapa="mob", monstro=None):
    resultado = jogar_fase(jogador, numero, etapa, monstro)
    if resultado == "salvou":
        return True

    if resultado == "vitoria":
        if numero == jogador["fase"] and numero < len(FASES):
            jogador["fase"] += 1
            print(f"\nNova fase liberada: {FASES[numero + 1]['nome']}!")
        if numero == len(FASES):
            print("\nVocê derrotou todos os chefes. Fim de jogo!")
            exibir_resumo(jogador)

    salvar_jogo(jogador, None)
    return False


def exibir_equipamentos(jogador):
    print("\n===== Equipamentos =====")
    for tipo in ARMAS:
        item = jogador["equipamentos"].get(tipo)
        print(f"{tipo}: {descrever(item) if item else 'vazio'}")


def exibir_resumo(jogador):
    stats = jogador["stats"]
    print("\n===== Resumo =====")
    print(f"Jogador: {jogador['nome']} ({jogador['classe']}), level {jogador['level']}")
    print(f"Níveis ganhos: {stats['niveis']}")
    print(f"Poções usadas: {stats['pocoes_usadas']}")
    print(f"Turnos jogados: {stats['turnos']}")
    print(f"Ouro acumulado: {jogador['ouro']}")


def menu_mapa(jogador):
    while True:
        print(f"\n===== Mapa | {jogador['nome']} | Level {jogador['level']} | "
              f"Ouro {jogador['ouro']} =====")
        for numero in range(1, jogador["fase"] + 1):
            print(f"[{numero}] {FASES[numero]['nome']}")
        print("[E] Equipamentos  [0] Salvar e sair")
        escolha = input("Fase: ").strip().lower()

        if escolha == "0":
            return None
        if escolha == "e":
            exibir_equipamentos(jogador)
        elif escolha.isdigit() and 1 <= int(escolha) <= jogador["fase"]:
            return int(escolha)
        else:
            print("Opção inválida.")


def caminho_save(nome):
    arquivo = "".join(letra for letra in nome if letra.isalnum()).lower() or "heroi"
    return os.path.join(PASTA_SAVES, f"{arquivo}.json")


def salvar_jogo(jogador, batalha):
    os.makedirs(PASTA_SAVES, exist_ok=True)
    with open(caminho_save(jogador["nome"]), "w", encoding="utf-8") as arquivo:
        json.dump({"jogador": jogador, "batalha": batalha}, arquivo, indent=2, ensure_ascii=False)


def ler_save(caminho):
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        jogador = dados["jogador"]
        dados["batalha"]
        jogador["fase"], jogador["stats"], jogador["equipamentos"]
        return dados
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        return None


def listar_saves():
    if not os.path.isdir(PASTA_SAVES):
        return []
    saves = []
    for arquivo in sorted(os.listdir(PASTA_SAVES)):
        caminho = os.path.join(PASTA_SAVES, arquivo)
        dados = ler_save(caminho) if arquivo.endswith(".json") else None
        if dados:
            saves.append((caminho, dados))
    return saves


def escolher_save(titulo):
    saves = listar_saves()
    if not saves:
        print("\nNenhum save encontrado.")
        return None

    print(f"\n===== {titulo} =====")
    for posicao, (_, dados) in enumerate(saves, start=1):
        jogador = dados["jogador"]
        print(f"[{posicao}] {jogador['nome']} | {jogador['classe']} | "
              f"Level {jogador['level']} | Fase {jogador['fase']}")
    print("[0] Voltar")

    while True:
        escolha = input("Save: ")
        if escolha == "0":
            return None
        if escolha.isdigit() and 1 <= int(escolha) <= len(saves):
            return saves[int(escolha) - 1]
        print("Opção inválida.")


def apagar_save():
    save = escolher_save("Apagar save")
    if save and input("Tem certeza? (s/n): ").lower() == "s":
        os.remove(save[0])
        print("Save apagado.")


def novo_jogo():
    nome = input("Digite o nome do jogador: ").strip() or "Herói"
    if os.path.exists(caminho_save(nome)):
        if input("Já existe um save com esse nome. Sobrescrever? (s/n): ").lower() != "s":
            return None

    print("\n[1] Guerreiro  [2] Mago  [3] Arqueiro")
    escolha = input("Classe: ")
    while escolha not in CLASSES:
        escolha = input("Opção inválida. Classe (1, 2 ou 3): ")
    return criar_jogador(nome, CLASSES[escolha])


def menu_inicial():
    while True:
        print("\n===== RPG de Batalha =====")
        print("[1] Novo jogo")
        print("[2] Continuar jogo salvo")
        print("[3] Apagar save")
        opcao = input("Opção: ")

        if opcao == "1":
            jogador = novo_jogo()
            if jogador:
                return jogador, None
        elif opcao == "2":
            save = escolher_save("Continuar")
            if save:
                return save[1]["jogador"], save[1]["batalha"]
        elif opcao == "3":
            apagar_save()
        else:
            print("Opção inválida.")


def iniciar_jogo():
    jogador, batalha = menu_inicial()

    if batalha:
        if processar_fase(jogador, batalha["fase"], batalha["etapa"], batalha["monstro"]):
            return

    while True:
        numero = menu_mapa(jogador)
        if numero is None:
            salvar_jogo(jogador, None)
            exibir_resumo(jogador)
            print("\nProgresso salvo.")
            return
        if processar_fase(jogador, numero):
            return


if __name__ == "__main__":
    iniciar_jogo()
