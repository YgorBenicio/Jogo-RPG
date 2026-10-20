import unittest
from unittest.mock import patch

import main
from dados import EFEITOS, FASES
from testes.apoio import entradas, novo_jogador


class TestStatus(unittest.TestCase):
    def setUp(self):
        self.jogador = novo_jogador("1")

    def aplicar(self):
        with entradas() as saida:
            main.aplicar_efeitos(self.jogador)
        return saida.getvalue()

    def test_sangramento_causa_dano_por_tres_turnos(self):
        with entradas():
            main.aplicar_status(self.jogador, "sangramento")
        total = 0
        for _ in range(5):
            antes = self.jogador["vida"]
            self.aplicar()
            total += antes - self.jogador["vida"]
        self.assertEqual(total, EFEITOS["sangramento"]["dano"] * 3)
        self.assertEqual(self.jogador["efeitos"], {})

    def test_varios_status_ao_mesmo_tempo(self):
        with entradas():
            main.aplicar_status(self.jogador, "sangramento")
            main.aplicar_status(self.jogador, "veneno")
        self.assertEqual(set(self.jogador["efeitos"]), {"sangramento", "veneno"})
        self.aplicar()
        esperado = EFEITOS["sangramento"]["dano"] + EFEITOS["veneno"]["dano"]
        self.assertEqual(self.jogador["vida"], 120 - esperado)

    def test_status_diferentes_expiram_cada_um_no_seu_tempo(self):
        self.jogador["efeitos"] = {"sangramento": 1, "veneno": 3}
        saida = self.aplicar()
        self.assertEqual(self.jogador["efeitos"], {"veneno": 2})
        self.assertIn("Sangramento passou", saida)

    def test_aplicar_de_novo_renova_a_duracao(self):
        self.jogador["efeitos"] = {"veneno": 1}
        with entradas():
            main.aplicar_status(self.jogador, "veneno")
        self.assertEqual(self.jogador["efeitos"]["veneno"], EFEITOS["veneno"]["turnos"])

    def test_status_pode_derrotar_o_jogador(self):
        self.jogador["vida"] = 3
        self.jogador["efeitos"] = {"sangramento": 3}
        self.aplicar()
        self.assertLessEqual(self.jogador["vida"], 0)

    def test_restaurar_limpa_os_status_e_recupera_vida_e_mana(self):
        self.jogador["efeitos"] = {"frio": 2}
        self.jogador["vida"], self.jogador["mana"] = 5, 0
        main.restaurar(self.jogador)
        self.assertEqual(self.jogador["efeitos"], {})
        self.assertEqual(self.jogador["vida"], self.jogador["vida_max"])
        self.assertEqual(self.jogador["mana"], self.jogador["mana_max"])


class TestStatusDosMonstros(unittest.TestCase):
    def test_todo_especial_usa_status_que_existem(self):
        for fase in FASES.values():
            for etapa in ("mob", "boss"):
                if etapa in fase:
                    for nome in fase[etapa]["especial"]["efeitos"]:
                        self.assertIn(nome, EFEITOS)

    def test_lobo_causa_sangramento(self):
        self.assertIn("sangramento", FASES[1]["mob"]["especial"]["efeitos"])

    def test_chefes_aplicam_mais_de_um_status(self):
        for numero in (1, 2, 3, 4, 5, 6):
            self.assertGreaterEqual(len(FASES[numero]["boss"]["especial"]["efeitos"]), 2)

    def test_especial_de_chefe_pode_aplicar_varios_status_de_uma_vez(self):
        jogador = novo_jogador("1")
        monstro = {"nome": "Chefe", "vida": 100, "vida_max": 100, "dano": 10,
                   "especial": FASES[1]["boss"]["especial"], "preparando": True}
        with patch.object(main, "sortear", return_value=True), entradas():
            main.turno_do_monstro(jogador, monstro, False)
        self.assertEqual(set(jogador["efeitos"]), {"sangramento", "veneno"})


if __name__ == "__main__":
    unittest.main()
