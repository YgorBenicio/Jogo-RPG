import statistics
import unittest

from testes.apoio import jogar_partida

SEMENTES = range(6)
CLASSES = ("1", "2", "3")


def simular(cuidadoso, com_secreta=False):
    return [jogar_partida(classe, semente, cuidadoso, com_secreta)
            for classe in CLASSES for semente in SEMENTES]


class TestDificuldadeEstiloSouls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cuidadoso = simular(True)
        cls.descuidado = simular(False)

    def test_e_possivel_zerar_o_jogo_com_qualquer_classe(self):
        self.assertTrue(all(partida["zerou"] for partida in self.cuidadoso))

    def test_e_possivel_zerar_sem_comprar_nada_na_loja(self):
        self.assertNotIn("Poção comprada", "".join(p["saida"] for p in self.cuidadoso))

    def test_o_jogo_e_dificil_e_o_jogador_morre_no_caminho(self):
        media = statistics.mean(p["mortes"] for p in self.cuidadoso)
        self.assertGreaterEqual(media, 1.5)

    def test_mas_nao_e_injusto(self):
        media = statistics.mean(p["mortes"] for p in self.cuidadoso)
        self.assertLessEqual(media, 12)

    def test_defender_nos_avisos_do_chefe_compensa(self):
        com_defesa = statistics.mean(p["mortes"] for p in self.cuidadoso)
        sem_defesa = statistics.mean(p["mortes"] for p in self.descuidado)
        self.assertLess(com_defesa, sem_defesa)

    def test_mesmo_sem_defender_ainda_da_para_vencer_treinando(self):
        self.assertTrue(all(partida["zerou"] for partida in self.descuidado))

    def test_chefe_secreto_tambem_pode_ser_vencido(self):
        partidas = simular(True, com_secreta=True)
        self.assertTrue(all(partida["secreta"] for partida in partidas))

    def test_mesma_semente_gera_a_mesma_partida(self):
        a = jogar_partida("1", 3, True)
        b = jogar_partida("1", 3, True)
        self.assertEqual((a["mortes"], a["turnos"], a["level"]), (b["mortes"], b["turnos"], b["level"]))


if __name__ == "__main__":
    unittest.main()
