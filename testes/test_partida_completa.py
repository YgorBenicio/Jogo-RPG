import unittest

from testes.apoio import jogar_partida


class TestPartidaCompleta(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.partida = jogar_partida("1", 7, cuidadoso=True, com_secreta=True)
        cls.saida = cls.partida["saida"]
        cls.descuidada = jogar_partida("1", 7, cuidadoso=False)["saida"]

    def test_o_jogo_foi_zerado_e_a_fase_secreta_vencida(self):
        self.assertTrue(self.partida["zerou"])
        self.assertTrue(self.partida["secreta"])

    def test_aparecem_as_cinco_fases_e_a_secreta(self):
        for nome in ("Floresta Sombria", "Deserto Escaldante", "Vulcão Ardente",
                     "Cripta Esquecida", "Montanha Gelada", "Abismo Esquecido"):
            self.assertIn(f": {nome} #", self.saida)

    def test_aparecem_monstros_e_chefes(self):
        for nome in ("Lobo", "Lobo Alfa", "Dragão de Gelo", "Guardião do Abismo"):
            self.assertIn(f"vs {nome} =", self.saida)

    def test_mecanicas_do_combate_aparecem_na_partida(self):
        for trecho in ("Acerto crítico!", "errou o ataque", "se prepara para usar",
                       "ATENÇÃO", "Você se prepara para o próximo golpe", "Lava cai do teto"):
            self.assertIn(trecho, self.saida, trecho)

    def test_status_aparecem_quando_o_jogador_nao_se_defende(self):
        for status in ("Sangramento", "Veneno", "Queimadura"):
            self.assertIn(f"Você está com {status}!", self.descuidada)

    def test_defender_nos_avisos_protege_contra_os_status(self):
        self.assertNotIn("Você está com", self.saida)

    def test_progressao_loja_bau_e_morte(self):
        for trecho in ("Subiu para o level", "Nova fase liberada", "Loja | Ouro",
                       "O chefe deixou um baú!", "VOCÊ MORREU", "Você perdeu"):
            self.assertIn(trecho, self.saida, trecho)

    def test_final_do_jogo(self):
        for trecho in ("Fim de jogo!", "Fase secreta liberada", "Resumo", "Progresso salvo."):
            self.assertIn(trecho, self.saida, trecho)

    def test_partida_termina_com_o_recorde_registrado(self):
        self.assertGreater(self.partida["turnos"], 0)


if __name__ == "__main__":
    unittest.main()
