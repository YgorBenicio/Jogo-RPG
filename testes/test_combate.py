import unittest
from unittest.mock import patch

import main
from testes.apoio import (
    dano_maximo, entradas, equipar, monstro_de_teste, novo_jogador, pasta_temporaria, sorteios,
)


class TestAtaqueNormal(unittest.TestCase):
    def setUp(self):
        self.jogador = novo_jogador("1")
        self.monstro = monstro_de_teste()

    def agir(self, *respostas):
        with entradas(*respostas) as saida:
            resultado = main.turno_do_jogador(self.jogador, self.monstro)
        return resultado, saida.getvalue()

    def test_dano_fica_entre_metade_e_o_dano_maximo(self):
        with patch.object(main, "sortear", return_value=False):
            for _ in range(100):
                self.monstro["vida"] = 100
                self.agir("1")
                dano = 100 - self.monstro["vida"]
                self.assertTrue(8 <= dano <= 16, dano)

    def test_ataque_pode_errar(self):
        with sorteios(True):
            resultado, saida = self.agir("1")
        self.assertEqual(self.monstro["vida"], 100)
        self.assertEqual(resultado, "ok")
        self.assertIn("errou", saida)

    def test_acerto_critico_dobra_o_dano(self):
        with dano_maximo(), sorteios(False, True):
            _, saida = self.agir("1")
        self.assertEqual(self.monstro["vida"], 100 - 32)
        self.assertIn("crítico", saida)

    def test_chance_base_de_critico_e_dez_por_cento(self):
        with dano_maximo(), sorteios(False, False) as falso:
            self.agir("1")
        self.assertEqual([chamada.args[0] for chamada in falso.call_args_list], [10, 10])


class TestAtaqueEspecial(unittest.TestCase):
    def setUp(self):
        self.jogador = novo_jogador("1")
        self.monstro = monstro_de_teste()

    def test_gasta_dez_de_mana_e_causa_dano_entre_o_dano_e_o_dobro(self):
        for _ in range(100):
            self.jogador["mana"] = 20
            self.monstro["vida"] = 100
            with entradas("2"):
                main.turno_do_jogador(self.jogador, self.monstro)
            self.assertEqual(self.jogador["mana"], 10)
            self.assertTrue(16 <= 100 - self.monstro["vida"] <= 32)

    def test_sem_mana_nao_gasta_o_turno(self):
        self.jogador["mana"] = 9
        with entradas("2") as saida:
            resultado = main.turno_do_jogador(self.jogador, self.monstro)
        self.assertEqual(resultado, "invalido")
        self.assertEqual(self.monstro["vida"], 100)
        self.assertIn("Mana insuficiente", saida.getvalue())

    def test_especial_nunca_erra(self):
        with patch.object(main, "sortear", side_effect=AssertionError):
            with entradas("2"):
                main.turno_do_jogador(self.jogador, self.monstro)
        self.assertLess(self.monstro["vida"], 100)


class TestOutrasAcoes(unittest.TestCase):
    def setUp(self):
        self.jogador = novo_jogador("1")
        self.monstro = monstro_de_teste()

    def agir(self, escolha):
        with entradas(escolha) as saida:
            return main.turno_do_jogador(self.jogador, self.monstro), saida.getvalue()

    def test_defender_avisa_a_batalha(self):
        resultado, _ = self.agir("3")
        self.assertEqual(resultado, "defesa")
        self.assertEqual(self.monstro["vida"], 100)

    def test_pocao_de_vida_cura_cinquenta(self):
        self.jogador["vida"] = 30
        resultado, _ = self.agir("4")
        self.assertEqual(resultado, "ok")
        self.assertEqual(self.jogador["vida"], 80)
        self.assertEqual(self.jogador["pocoes_vida"], 1)
        self.assertEqual(self.jogador["stats"]["pocoes_usadas"], 1)

    def test_pocao_de_vida_nao_passa_do_maximo(self):
        self.jogador["vida"] = self.jogador["vida_max"] - 10
        self.agir("4")
        self.assertEqual(self.jogador["vida"], self.jogador["vida_max"])

    def test_sem_pocao_de_vida_nao_gasta_o_turno(self):
        self.jogador["pocoes_vida"] = 0
        resultado, saida = self.agir("4")
        self.assertEqual(resultado, "invalido")
        self.assertIn("não tem poções de vida", saida)

    def test_pocao_de_mana_recupera_trinta(self):
        self.jogador["mana"] = 0
        resultado, _ = self.agir("5")
        self.assertEqual(resultado, "ok")
        self.assertEqual(self.jogador["mana"], 20)
        self.assertEqual(self.jogador["pocoes_mana"], 0)

    def test_sem_pocao_de_mana_nao_gasta_o_turno(self):
        self.jogador["pocoes_mana"] = 0
        resultado, _ = self.agir("5")
        self.assertEqual(resultado, "invalido")

    def test_opcao_invalida_nao_gasta_o_turno(self):
        resultado, saida = self.agir("x")
        self.assertEqual(resultado, "invalido")
        self.assertIn("Opção inválida", saida)

    def test_salvar_e_sair(self):
        resultado, _ = self.agir("6")
        self.assertEqual(resultado, "sair")


class TestTurnoDoMonstro(unittest.TestCase):
    def setUp(self):
        self.jogador = novo_jogador("1")
        self.monstro = monstro_de_teste()

    def turno(self, defendendo=False):
        with entradas() as saida:
            main.turno_do_monstro(self.jogador, self.monstro, defendendo)
        return saida.getvalue()

    def test_monstro_pode_errar(self):
        with sorteios(False, True):
            saida = self.turno()
        self.assertEqual(self.jogador["vida"], 120)
        self.assertIn("errou", saida)

    def test_ataque_normal_causa_dano(self):
        with dano_maximo(), sorteios(False, False):
            self.turno()
        self.assertEqual(self.jogador["vida"], 110)

    def test_monstro_avisa_antes_de_usar_o_especial(self):
        with sorteios(True):
            saida = self.turno()
        self.assertTrue(self.monstro["preparando"])
        self.assertEqual(self.jogador["vida"], 120)
        self.assertIn("se prepara", saida)

    def test_especial_e_usado_no_turno_seguinte_com_dano_multiplicado(self):
        self.monstro["preparando"] = True
        with dano_maximo(), sorteios(False):
            saida = self.turno()
        self.assertFalse(self.monstro["preparando"])
        self.assertEqual(self.jogador["vida"], 120 - 20)
        self.assertIn("usou Golpe Forte", saida)

    def test_especial_aplica_status(self):
        self.monstro["preparando"] = True
        with dano_maximo(), sorteios(True):
            self.turno()
        self.assertIn("sangramento", self.jogador["efeitos"])

    def test_defender_reduz_o_dano_pela_metade(self):
        with dano_maximo(), sorteios(False, False):
            self.turno(defendendo=True)
        self.assertEqual(self.jogador["vida"], 115)

    def test_defender_bloqueia_o_status_do_especial(self):
        self.monstro["preparando"] = True
        with dano_maximo():
            self.turno(defendendo=True)
        self.assertEqual(self.jogador["efeitos"], {})
        self.assertEqual(self.jogador["vida"], 120 - 10)

    def test_dano_minimo_e_um(self):
        equipar(self.jogador, "Escudo", nivel=60)
        with dano_maximo(), sorteios(False, False):
            self.turno()
        self.assertEqual(self.jogador["vida"], 119)

    def test_monstro_atordoado_perde_o_turno_e_cancela_o_preparo(self):
        self.monstro["atordoado"] = True
        self.monstro["preparando"] = True
        saida = self.turno()
        self.assertEqual(self.jogador["vida"], 120)
        self.assertFalse(self.monstro["preparando"])
        self.assertFalse(self.monstro["atordoado"])
        self.assertIn("atordoado", saida)


class TestEventoDoAmbiente(unittest.TestCase):
    EVENTO = {"nome": "Lava cai do teto", "chance": 100, "dano": 20}

    def setUp(self):
        self.jogador = novo_jogador("1")
        self.monstro = monstro_de_teste()

    def evento(self, alvo, sorteio=True):
        with patch.object(main, "sortear", return_value=sorteio), \
                patch.object(main, "choice", return_value=alvo), dano_maximo(), entradas() as saida:
            main.aplicar_evento(self.EVENTO, self.jogador, self.monstro)
        return saida.getvalue()

    def test_evento_pode_atingir_o_jogador(self):
        saida = self.evento("jogador")
        self.assertEqual(self.jogador["vida"], 100)
        self.assertEqual(self.monstro["vida"], 100)
        self.assertIn("Lava cai do teto", saida)

    def test_evento_pode_atingir_o_monstro(self):
        self.evento("monstro")
        self.assertEqual(self.jogador["vida"], 120)
        self.assertEqual(self.monstro["vida"], 80)

    def test_evento_nem_sempre_acontece(self):
        saida = self.evento("jogador", sorteio=False)
        self.assertEqual(self.jogador["vida"], 120)
        self.assertEqual(saida, "")


class TestBatalha(unittest.TestCase):
    def batalhar(self, jogador, monstro, *respostas):
        with entradas(*respostas) as saida, patch.object(main, "sortear", return_value=False):
            resultado = main.batalhar(jogador, monstro, 1, "mob")
        return resultado, saida.getvalue()

    def test_jogador_vence_quando_a_vida_do_monstro_acaba(self):
        jogador = novo_jogador("1")
        monstro = monstro_de_teste(vida=1, vida_max=1)
        resultado, _ = self.batalhar(jogador, monstro, "1")
        self.assertEqual(resultado, "vitoria")

    def test_jogador_perde_quando_a_vida_acaba(self):
        jogador = novo_jogador("1")
        jogador["vida"] = 1
        monstro = monstro_de_teste(dano=50)
        with dano_maximo():
            resultado, _ = self.batalhar(jogador, monstro, "3")
        self.assertEqual(resultado, "derrota")

    def test_monstro_morto_nao_contra_ataca(self):
        jogador = novo_jogador("1")
        monstro = monstro_de_teste(vida=1, vida_max=1)
        self.batalhar(jogador, monstro, "1")
        self.assertEqual(jogador["vida"], jogador["vida_max"])

    def test_acao_invalida_nao_conta_turno(self):
        jogador = novo_jogador("1")
        monstro = monstro_de_teste(vida=1, vida_max=1)
        self.batalhar(jogador, monstro, "x", "9", "1")
        self.assertEqual(jogador["stats"]["turnos"], 1)

    def test_cada_acao_valida_conta_um_turno(self):
        jogador = novo_jogador("1")
        monstro = monstro_de_teste(vida=1000, vida_max=1000)
        with self.assertRaises(EOFError):
            self.batalhar(jogador, monstro, "1", "1", "3")
        self.assertEqual(jogador["stats"]["turnos"], 3)

    def test_painel_mostra_o_aviso_do_especial(self):
        jogador = novo_jogador("1")
        monstro = monstro_de_teste(preparando=True)
        with entradas("6") as saida, pasta_temporaria():
            main.batalhar(jogador, monstro, 1, "mob")
        self.assertIn("ATENÇÃO", saida.getvalue())
        self.assertIn("Golpe Forte", saida.getvalue())

    def test_salvar_e_sair_guarda_a_luta_no_ponto_exato(self):
        jogador = novo_jogador("1", "Luta")
        monstro = monstro_de_teste(vida=77, preparando=True)
        with entradas("6"), pasta_temporaria():
            resultado = main.batalhar(jogador, monstro, 2, "boss")
            batalha = main.listar_saves()[0][1]["batalha"]
        self.assertEqual(resultado, "salvou")
        self.assertEqual(batalha["fase"], 2)
        self.assertEqual(batalha["etapa"], "boss")
        self.assertEqual(batalha["monstro"]["vida"], 77)
        self.assertTrue(batalha["monstro"]["preparando"])


if __name__ == "__main__":
    unittest.main()
