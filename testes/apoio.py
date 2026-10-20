import io
import random
import tempfile
from contextlib import contextmanager, redirect_stdout
from unittest.mock import patch

import main
from dados import CLASSES, FASE_SECRETA, ULTIMA_FASE


def novo_jogador(classe="1", nome="Teste"):
    return main.criar_jogador(nome, CLASSES[classe])


def monstro_de_teste(**mudancas):
    monstro = {
        "nome": "Alvo", "vida": 100, "vida_max": 100, "dano": 10, "exp": 10, "ouro": 10,
        "especial": {"nome": "Golpe Forte", "chance": 0, "multiplicador": 2,
                     "efeitos": ["sangramento"], "chance_efeito": 100},
    }
    monstro.update(mudancas)
    return monstro


def item_de_teste(tipo="Espada", tier=1, nivel=10):
    return {"nome": f"{tipo} de teste", "tipo": tipo, "tier": tier, "nivel": nivel}


def equipar(jogador, tipo, tier=1, nivel=10):
    jogador["equipamentos"][tipo] = item_de_teste(tipo, tier, nivel)


@contextmanager
def entradas(*respostas):
    fila = list(respostas)

    def falso(prompt=""):
        if not fila:
            raise EOFError("as entradas simuladas acabaram")
        resposta = fila.pop(0)
        print(f"{prompt}{resposta}")
        return resposta

    saida = io.StringIO()
    with patch("builtins.input", falso), redirect_stdout(saida):
        yield saida


@contextmanager
def pasta_temporaria():
    with tempfile.TemporaryDirectory() as pasta:
        with patch.object(main, "PASTA_SAVES", pasta):
            yield pasta


@contextmanager
def sorteios(*resultados):
    with patch.object(main, "sortear", side_effect=list(resultados)) as falso:
        yield falso


@contextmanager
def dano_maximo():
    with patch.object(main, "randint", side_effect=lambda minimo, maximo: maximo):
        yield


def escolher_acao(jogador, monstro, cuidadoso):
    if cuidadoso and monstro.get("preparando"):
        return "3"
    if jogador["vida"] < jogador["vida_max"] * 0.4 and jogador["pocoes_vida"] > 0:
        return "4"
    if jogador["mana"] >= main.CUSTO_ESPECIAL:
        return "2"
    if jogador["pocoes_mana"] > 0:
        return "5"
    return "1"


def jogar_partida(classe, semente, cuidadoso=True, com_secreta=False, limite=3000):
    random.seed(semente)
    estado = {"jogador": None, "monstro": None, "item": None, "mortes": 0,
              "seguidas": 0, "secreta": False, "chamadas": 0}

    original_status = main.exibir_status
    original_oferta = main.oferecer_item
    original_fase = main.jogar_fase
    original_criar = main.criar_jogador

    def espiar_criar(nome, classe):
        estado["jogador"] = original_criar(nome, classe)
        return estado["jogador"]

    def espiar_status(jogador, monstro):
        estado["jogador"], estado["monstro"] = jogador, monstro
        original_status(jogador, monstro)

    def espiar_oferta(jogador, item):
        estado["item"] = item
        return original_oferta(jogador, item)

    def espiar_fase(jogador, numero, *argumentos):
        resultado = original_fase(jogador, numero, *argumentos)
        if resultado == "derrota":
            estado["mortes"] += 1
            estado["seguidas"] += 1
        elif resultado == "vitoria":
            estado["seguidas"] = 0
            estado["secreta"] = estado["secreta"] or numero == FASE_SECRETA
        return resultado

    def responder(prompt=""):
        estado["chamadas"] += 1
        if estado["chamadas"] > limite * 100:
            raise RuntimeError("partida não terminou")
        jogador = estado["jogador"]
        if prompt == "Opção: ":
            return "1"
        if prompt == "Digite o nome do jogador: ":
            return "Bot"
        if prompt == "Classe: ":
            return classe
        if prompt == "Ação: ":
            return escolher_acao(jogador, estado["monstro"], cuidadoso)
        if prompt == "Comprar: ":
            return "0"
        if prompt.startswith("Trocar"):
            atual = jogador["equipamentos"][estado["item"]["tipo"]]
            return "s" if estado["item"]["nivel"] > atual["nivel"] else "n"
        if prompt == "Fase: ":
            if jogador["zerou_em"] is not None:
                if not com_secreta or estado["secreta"]:
                    return "0"
                return str(ULTIMA_FASE) if estado["seguidas"] >= 2 else str(FASE_SECRETA)
            alvo = jogador["fase"]
            if estado["seguidas"] >= 2:
                alvo = random.randint(max(1, alvo - 2), alvo)
            return str(alvo)
        raise AssertionError(f"pergunta inesperada: {prompt!r}")

    saida = io.StringIO()
    with pasta_temporaria(), patch("builtins.input", responder), redirect_stdout(saida), \
            patch.object(main, "exibir_status", espiar_status), \
            patch.object(main, "oferecer_item", espiar_oferta), \
            patch.object(main, "jogar_fase", espiar_fase), \
            patch.object(main, "criar_jogador", espiar_criar):
        main.iniciar_jogo()

    jogador = estado["jogador"]
    return {
        "zerou": jogador is not None and jogador["zerou_em"] is not None,
        "mortes": estado["mortes"],
        "level": jogador["level"] if jogador else 0,
        "turnos": jogador["stats"]["turnos"] if jogador else 0,
        "secreta": estado["secreta"],
        "saida": saida.getvalue(),
    }
