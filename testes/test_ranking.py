import unittest

import main
from testes.apoio import entradas, novo_jogador, pasta_temporaria


def salvar(nome, classe, zerou_em):
    jogador = novo_jogador(classe, nome)
    jogador["zerou_em"] = zerou_em
    main.salvar_jogo(jogador, None)


class TestRanking(unittest.TestCase):
    def ranking(self):
        with entradas() as saida:
            main.exibir_ranking()
        return saida.getvalue()

    def test_sem_ninguem_que_tenha_zerado(self):
        with pasta_temporaria():
            salvar("Ana", "1", None)
            self.assertIn("Ninguém zerou", self.ranking())

    def test_ordena_por_menos_turnos(self):
        with pasta_temporaria():
            salvar("Lenta", "1", 300)
            salvar("Rapida", "2", 90)
            salvar("Media", "3", 150)
            linhas = [l for l in self.ranking().splitlines() if l[:2] in ("1.", "2.", "3.")]
        self.assertEqual([l.split()[1] for l in linhas], ["Rapida", "Media", "Lenta"])
        self.assertIn("90 turnos", linhas[0])

    def test_quem_nao_zerou_fica_de_fora(self):
        with pasta_temporaria():
            salvar("Campea", "1", 100)
            salvar("Iniciante", "1", None)
            saida = self.ranking()
        self.assertIn("Campea", saida)
        self.assertNotIn("Iniciante", saida)

    def test_mostra_a_classe(self):
        with pasta_temporaria():
            salvar("Ana", "2", 80)
            self.assertIn("Ana (Mago)", self.ranking())

    def test_mostra_so_os_dez_melhores(self):
        with pasta_temporaria():
            for numero in range(12):
                salvar(f"Jogador{numero:02d}", "1", 100 + numero)
            saida = self.ranking()
        self.assertIn("Jogador09", saida)
        self.assertNotIn("Jogador10", saida)

    def test_ranking_aparece_no_menu_inicial(self):
        with pasta_temporaria():
            salvar("Ana", "1", 70)
            with entradas("4", "0") as saida:
                main.menu_inicial()
        self.assertIn("Ranking", saida.getvalue())
        self.assertIn("1. Ana", saida.getvalue())

    def test_recorde_sobrevive_ao_salvar_e_carregar(self):
        with pasta_temporaria():
            salvar("Ana", "1", 77)
            self.assertEqual(main.listar_saves()[0][1]["jogador"]["zerou_em"], 77)


if __name__ == "__main__":
    unittest.main()
