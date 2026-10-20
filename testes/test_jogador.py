import unittest

import main
from dados import CLASSES
from testes.apoio import entradas, novo_jogador


class TestCriacaoDoJogador(unittest.TestCase):
    def test_cada_classe_nasce_com_os_atributos_da_tabela(self):
        for chave, classe in CLASSES.items():
            jogador = main.criar_jogador("Ana", classe)
            self.assertEqual(jogador["classe"], classe["nome"])
            self.assertEqual(jogador["vida"], classe["vida"])
            self.assertEqual(jogador["vida_max"], classe["vida"])
            self.assertEqual(jogador["mana"], classe["mana"])
            self.assertEqual(jogador["dano"], classe["dano"])

    def test_estado_inicial(self):
        jogador = novo_jogador()
        self.assertEqual(jogador["level"], 1)
        self.assertEqual(jogador["fase"], 1)
        self.assertEqual(jogador["ouro"], 0)
        self.assertEqual(jogador["efeitos"], {})
        self.assertEqual(jogador["equipamentos"], {})
        self.assertIsNone(jogador["zerou_em"])
        self.assertEqual(jogador["stats"], {"niveis": 0, "pocoes_usadas": 0, "turnos": 0})


class TestSorteio(unittest.TestCase):
    def test_chance_zero_nunca_acerta(self):
        self.assertFalse(any(main.sortear(0) for _ in range(200)))

    def test_chance_cem_sempre_acerta(self):
        self.assertTrue(all(main.sortear(100) for _ in range(200)))


class TestSubirDeNivel(unittest.TestCase):
    def test_sem_experiencia_suficiente_nao_sobe(self):
        jogador = novo_jogador()
        jogador["exp"] = jogador["exp_max"] - 1
        with entradas():
            main.subir_de_nivel(jogador)
        self.assertEqual(jogador["level"], 1)

    def test_experiencia_exata_sobe_um_nivel(self):
        jogador = novo_jogador()
        jogador["exp"] = jogador["exp_max"]
        with entradas():
            main.subir_de_nivel(jogador)
        self.assertEqual(jogador["level"], 2)
        self.assertEqual(jogador["exp"], 0)

    def test_excedente_de_experiencia_e_guardado(self):
        jogador = novo_jogador()
        jogador["exp"] = 25
        with entradas():
            main.subir_de_nivel(jogador)
        self.assertEqual(jogador["level"], 2)
        self.assertEqual(jogador["exp"], 5)

    def test_sobe_varios_niveis_de_uma_vez(self):
        jogador = novo_jogador()
        jogador["exp"] = 100
        with entradas():
            main.subir_de_nivel(jogador)
        self.assertEqual(jogador["level"], 4)
        self.assertEqual(jogador["exp"], 5)
        self.assertEqual(jogador["stats"]["niveis"], 3)

    def test_atributos_crescem_a_cada_nivel(self):
        jogador = novo_jogador()
        vida, mana, dano = jogador["vida_max"], jogador["mana_max"], jogador["dano"]
        jogador["exp"] = jogador["exp_max"]
        with entradas():
            main.subir_de_nivel(jogador)
        self.assertEqual(jogador["vida_max"], vida + 20)
        self.assertEqual(jogador["mana_max"], mana + 5)
        self.assertEqual(jogador["dano"], dano + 4)

    def test_experiencia_necessaria_aumenta(self):
        jogador = novo_jogador()
        antes = jogador["exp_max"]
        jogador["exp"] = antes
        with entradas():
            main.subir_de_nivel(jogador)
        self.assertGreater(jogador["exp_max"], antes)


if __name__ == "__main__":
    unittest.main()
