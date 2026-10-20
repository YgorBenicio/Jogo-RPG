import random
import unittest
from unittest.mock import patch

import main
from dados import ARMAS, BAU_TIERS, EXTRAS, FASES, TIERS
from testes.apoio import (
    dano_maximo, entradas, equipar, item_de_teste, monstro_de_teste, novo_jogador, sorteios,
)


class TestBonusDasArmas(unittest.TestCase):
    def setUp(self):
        self.jogador = novo_jogador("1")
        self.monstro = monstro_de_teste()

    def atacar(self):
        with entradas("1"), dano_maximo(), sorteios(False, False):
            main.turno_do_jogador(self.jogador, self.monstro)
        return 100 - self.monstro["vida"]

    def test_espada_soma_metade_do_nivel_ao_ataque_normal(self):
        equipar(self.jogador, "Espada", nivel=20)
        self.assertEqual(self.atacar(), 16 + 10)

    def test_cajado_soma_o_nivel_ao_especial(self):
        equipar(self.jogador, "Cajado", nivel=20)
        with entradas("2"), dano_maximo():
            main.turno_do_jogador(self.jogador, self.monstro)
        self.assertEqual(100 - self.monstro["vida"], 32 + 20)

    def test_arco_aumenta_a_chance_de_critico(self):
        equipar(self.jogador, "Arco", nivel=30)
        with entradas("1"), dano_maximo(), sorteios(False, False) as falso:
            main.turno_do_jogador(self.jogador, self.monstro)
        self.assertEqual(falso.call_args_list[1].args[0], 10 + 15)

    def test_escudo_reduz_um_terco_do_nivel_do_dano_recebido(self):
        equipar(self.jogador, "Escudo", nivel=30)
        with dano_maximo(), sorteios(False, False), entradas():
            main.turno_do_monstro(self.jogador, self.monstro, False)
        self.assertEqual(self.jogador["vida"], 119)

    def test_sem_equipamento_nao_ha_bonus(self):
        self.assertEqual(self.atacar(), 16)


class TestExtrasDasArmas(unittest.TestCase):
    def setUp(self):
        self.jogador = novo_jogador("1")
        self.monstro = monstro_de_teste()

    def test_tier_um_nao_tem_extra(self):
        for tipo in ARMAS:
            equipar(self.jogador, tipo, tier=1)
            self.assertEqual(main.forca_extra(self.jogador, tipo), 0)

    def test_extra_cresce_com_o_tier(self):
        equipar(self.jogador, "Espada", tier=2)
        self.assertEqual(main.forca_extra(self.jogador, "Espada"), 20)
        equipar(self.jogador, "Espada", tier=3)
        self.assertEqual(main.forca_extra(self.jogador, "Espada"), 30)

    def test_todo_tipo_de_arma_tem_um_extra_descrito(self):
        self.assertEqual(set(EXTRAS), set(ARMAS))

    def test_espada_rouba_vida(self):
        equipar(self.jogador, "Espada", tier=3, nivel=0)
        self.jogador["vida"] = 50
        with entradas("1"), dano_maximo(), sorteios(False, False):
            main.turno_do_jogador(self.jogador, self.monstro)
        self.assertEqual(self.jogador["vida"], 50 + 16 * 30 // 100)

    def test_roubo_de_vida_nao_passa_da_vida_maxima(self):
        equipar(self.jogador, "Espada", tier=3, nivel=0)
        with entradas("1"), dano_maximo(), sorteios(False, False):
            main.turno_do_jogador(self.jogador, self.monstro)
        self.assertEqual(self.jogador["vida"], self.jogador["vida_max"])

    def test_arco_pode_atirar_duas_flechas(self):
        equipar(self.jogador, "Arco", tier=2, nivel=0)
        with entradas("1") as saida, dano_maximo(), sorteios(False, False, True):
            main.turno_do_jogador(self.jogador, self.monstro)
        self.assertEqual(self.monstro["vida"], 100 - 32)
        self.assertIn("Flecha dupla", saida.getvalue())

    def test_cajado_pode_atordoar_no_especial(self):
        equipar(self.jogador, "Cajado", tier=2, nivel=0)
        with entradas("2") as saida, sorteios(True):
            main.turno_do_jogador(self.jogador, self.monstro)
        self.assertTrue(self.monstro["atordoado"])
        self.assertIn("atordoado", saida.getvalue())

    def test_atordoamento_faz_o_monstro_perder_o_turno_na_batalha(self):
        equipar(self.jogador, "Cajado", tier=3, nivel=0)
        with entradas("2", "6") as saida, sorteios(True, False), patch.object(main, "salvar_jogo"):
            main.batalhar(self.jogador, self.monstro, 1, "mob")
        self.assertIn("perde o turno", saida.getvalue())
        self.assertEqual(self.jogador["vida"], 120)

    def test_escudo_reflete_parte_do_dano(self):
        equipar(self.jogador, "Escudo", tier=3, nivel=0)
        with dano_maximo(), sorteios(False, False), entradas() as saida:
            main.turno_do_monstro(self.jogador, self.monstro, False)
        self.assertEqual(self.monstro["vida"], 100 - 10 * 30 // 100)
        self.assertIn("Reflexo", saida.getvalue())


class TestBau(unittest.TestCase):
    def abrir(self, numero=1, jogador=None):
        jogador = jogador or novo_jogador("1")
        with entradas("n", "n", "n", "n"):
            main.abrir_bau(jogador, numero)
        return jogador

    def test_item_tem_tipo_tier_e_nivel_validos(self):
        random.seed(1)
        for numero in range(1, 7):
            for _ in range(60):
                jogador = self.abrir(numero)
                item = next(iter(jogador["equipamentos"].values()))
                minimo, maximo = TIERS[item["tier"]]
                self.assertIn(item["tipo"], ARMAS)
                self.assertTrue(minimo <= item["nivel"] <= maximo)

    def test_nome_do_item_leva_o_tema_da_fase(self):
        random.seed(2)
        for numero in range(1, 7):
            jogador = self.abrir(numero)
            item = next(iter(jogador["equipamentos"].values()))
            self.assertTrue(item["nome"].endswith(FASES[numero]["sufixo"]))

    def test_faixas_de_nivel_de_cada_tier(self):
        self.assertEqual(TIERS[1], (7, 22))
        self.assertEqual(len(TIERS), 3)
        self.assertLess(TIERS[1][1], TIERS[2][0])
        self.assertLess(TIERS[2][1], TIERS[3][0])

    def test_fases_avancadas_dao_tiers_melhores(self):
        random.seed(3)

        def media(numero):
            tiers = []
            for _ in range(400):
                jogador = self.abrir(numero)
                tiers.append(next(iter(jogador["equipamentos"].values()))["tier"])
            return sum(tiers) / len(tiers)

        self.assertLess(media(1), media(3))
        self.assertLess(media(3), media(5))

    def test_fase_secreta_nao_solta_tier_um(self):
        self.assertEqual(BAU_TIERS[6][0], 0)

    def test_refazer_a_fase_pode_dar_o_mesmo_tier_com_nivel_diferente(self):
        random.seed(4)
        niveis = set()
        for _ in range(300):
            jogador = self.abrir(1)
            item = next(iter(jogador["equipamentos"].values()))
            if item["tipo"] == "Espada" and item["tier"] == 1:
                niveis.add(item["nivel"])
        self.assertGreater(len(niveis), 3)


class TestTrocaDeEquipamento(unittest.TestCase):
    def test_slot_vazio_equipa_sem_perguntar(self):
        jogador = novo_jogador("1")
        item = item_de_teste("Arco", 1, 15)
        with entradas():
            self.assertTrue(main.oferecer_item(jogador, item))
        self.assertEqual(jogador["equipamentos"]["Arco"], item)

    def test_slot_ocupado_pergunta_e_troca_se_confirmar(self):
        jogador = novo_jogador("1")
        equipar(jogador, "Arco", nivel=10)
        novo = item_de_teste("Arco", 1, 20)
        with entradas("s"):
            self.assertTrue(main.oferecer_item(jogador, novo))
        self.assertEqual(jogador["equipamentos"]["Arco"]["nivel"], 20)

    def test_slot_ocupado_mantem_o_item_se_recusar(self):
        jogador = novo_jogador("1")
        equipar(jogador, "Arco", nivel=10)
        with entradas("n"):
            self.assertFalse(main.oferecer_item(jogador, item_de_teste("Arco", 1, 20)))
        self.assertEqual(jogador["equipamentos"]["Arco"]["nivel"], 10)

    def test_um_slot_por_tipo(self):
        jogador = novo_jogador("1")
        with entradas():
            for tipo in ARMAS:
                main.oferecer_item(jogador, item_de_teste(tipo))
        self.assertEqual(set(jogador["equipamentos"]), set(ARMAS))


class TestDescricao(unittest.TestCase):
    def test_descrever_mostra_nome_tier_e_nivel(self):
        item = {"nome": "Espada da Floresta", "tipo": "Espada", "tier": 2, "nivel": 31}
        self.assertEqual(main.descrever(item), "Espada da Floresta (Tier 2, nível 31)")

    def test_efeito_extra_so_aparece_do_tier_dois_em_diante(self):
        self.assertNotIn("extra", main.descrever_efeitos(item_de_teste("Espada", 1)))
        self.assertIn("extra", main.descrever_efeitos(item_de_teste("Espada", 2)))


if __name__ == "__main__":
    unittest.main()
