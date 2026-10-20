import unittest
from unittest.mock import patch

import main
from dados import FASES, LOJA, PRECO_POCAO_MANA, PRECO_POCAO_VIDA
from testes.apoio import entradas, equipar, novo_jogador


class TestDadosDaLoja(unittest.TestCase):
    def test_toda_fase_tem_loja_com_duas_armas(self):
        self.assertEqual(set(LOJA), set(FASES))
        for armas in LOJA.values():
            self.assertEqual(len(armas), 2)

    def test_armas_da_loja_sao_diferentes_em_cada_fase(self):
        nomes = [arma["nome"] for armas in LOJA.values() for arma in armas]
        self.assertEqual(len(nomes), len(set(nomes)))

    def test_armas_sao_caras(self):
        for armas in LOJA.values():
            for arma in armas:
                self.assertGreaterEqual(arma["preco"], 300)
                self.assertGreater(arma["preco"], PRECO_POCAO_VIDA * 10)

    def test_armas_mais_caras_nas_fases_mais_avancadas(self):
        menores = [min(arma["preco"] for arma in LOJA[numero]) for numero in sorted(LOJA)]
        self.assertEqual(menores, sorted(menores))

    def test_armas_da_loja_sao_tier_dois_ou_tres(self):
        for armas in LOJA.values():
            for arma in armas:
                self.assertIn(arma["tier"], (2, 3))


class TestComprar(unittest.TestCase):
    def setUp(self):
        self.jogador = novo_jogador("1")
        self.jogador["ouro"] = 500

    def comprar(self, *respostas, fase=1):
        with entradas(*respostas, "0") as saida:
            main.loja(self.jogador, fase)
        return saida.getvalue()

    def test_comprar_pocao_de_vida(self):
        self.comprar("1")
        self.assertEqual(self.jogador["pocoes_vida"], 3)
        self.assertEqual(self.jogador["ouro"], 500 - PRECO_POCAO_VIDA)

    def test_comprar_pocao_de_mana(self):
        self.comprar("2")
        self.assertEqual(self.jogador["pocoes_mana"], 2)
        self.assertEqual(self.jogador["ouro"], 500 - PRECO_POCAO_MANA)

    def test_sem_ouro_nao_compra_pocao(self):
        self.jogador["ouro"] = 10
        saida = self.comprar("1")
        self.assertEqual(self.jogador["pocoes_vida"], 2)
        self.assertEqual(self.jogador["ouro"], 10)
        self.assertIn("Ouro insuficiente", saida)

    def test_comprar_arma_equipa_e_desconta_o_preco(self):
        self.comprar("3")
        arma = LOJA[1][0]
        self.assertEqual(self.jogador["equipamentos"][arma["tipo"]]["nome"], arma["nome"])
        self.assertEqual(self.jogador["ouro"], 500 - arma["preco"])

    def test_sem_ouro_nao_compra_arma(self):
        self.jogador["ouro"] = LOJA[1][0]["preco"] - 1
        saida = self.comprar("3")
        self.assertEqual(self.jogador["equipamentos"], {})
        self.assertIn("Ouro insuficiente", saida)

    def test_recusar_a_troca_nao_cobra(self):
        arma = LOJA[1][0]
        equipar(self.jogador, arma["tipo"], nivel=5)
        self.comprar("3", "n")
        self.assertEqual(self.jogador["ouro"], 500)
        self.assertEqual(self.jogador["equipamentos"][arma["tipo"]]["nivel"], 5)

    def test_aceitar_a_troca_cobra(self):
        arma = LOJA[1][0]
        equipar(self.jogador, arma["tipo"], nivel=5)
        self.comprar("3", "s")
        self.assertEqual(self.jogador["ouro"], 500 - arma["preco"])
        self.assertEqual(self.jogador["equipamentos"][arma["tipo"]]["nivel"], arma["nivel"])

    def test_cada_fase_vende_as_suas_armas(self):
        self.jogador["ouro"] = 5000
        saida = self.comprar(fase=3)
        for arma in LOJA[3]:
            self.assertIn(arma["nome"], saida)
        self.assertNotIn(LOJA[1][0]["nome"], saida)

    def test_opcao_invalida(self):
        saida = self.comprar("9", "x")
        self.assertEqual(saida.count("Opção inválida"), 2)
        self.assertEqual(self.jogador["ouro"], 500)

    def test_comprar_a_mesma_arma_nao_altera_o_dicionario_da_loja(self):
        self.comprar("3")
        self.jogador["equipamentos"][LOJA[1][0]["tipo"]]["nivel"] = 1
        self.assertEqual(LOJA[1][0]["nivel"], 30)


class TestLojaAposVitoria(unittest.TestCase):
    def test_loja_abre_depois_de_cada_monstro_derrotado(self):
        jogador = novo_jogador("1")
        with patch.object(main, "batalhar", side_effect=["vitoria", "vitoria"]), \
                patch.object(main, "loja") as loja, patch.object(main, "abrir_bau"), \
                patch.object(main, "salvar_jogo"), entradas():
            main.jogar_fase(jogador, 1)
        self.assertEqual(loja.call_count, 2)
        loja.assert_called_with(jogador, 1)

    def test_loja_nao_abre_depois_de_uma_derrota(self):
        jogador = novo_jogador("1")
        with patch.object(main, "batalhar", return_value="derrota"), \
                patch.object(main, "loja") as loja, entradas():
            main.jogar_fase(jogador, 1)
        loja.assert_not_called()


if __name__ == "__main__":
    unittest.main()
