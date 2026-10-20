import unittest
from unittest.mock import patch

import main
from testes.apoio import entradas, monstro_de_teste, novo_jogador


class TestResumoFinal(unittest.TestCase):
    def test_resumo_mostra_niveis_pocoes_e_turnos(self):
        jogador = novo_jogador("1", "Ana")
        jogador["stats"] = {"niveis": 6, "pocoes_usadas": 9, "turnos": 211}
        with entradas() as saida:
            main.exibir_resumo(jogador)
        texto = saida.getvalue()
        self.assertIn("Níveis ganhos: 6", texto)
        self.assertIn("Poções usadas: 9", texto)
        self.assertIn("Turnos jogados: 211", texto)

    def test_estatisticas_sao_contadas_durante_o_jogo(self):
        jogador = novo_jogador("1")
        jogador["vida"] = 10
        monstro = monstro_de_teste(vida=1, vida_max=1)
        with entradas("4", "1"), patch.object(main, "sortear", return_value=False):
            main.batalhar(jogador, monstro, 1, "mob")
        self.assertEqual(jogador["stats"]["turnos"], 2)
        self.assertEqual(jogador["stats"]["pocoes_usadas"], 1)
        with entradas():
            main.receber_recompensa(jogador, monstro_de_teste(exp=100))
        self.assertGreaterEqual(jogador["stats"]["niveis"], 3)


if __name__ == "__main__":
    unittest.main()
