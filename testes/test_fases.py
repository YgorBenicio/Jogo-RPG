import unittest
from unittest.mock import patch

import main
from dados import FASE_SECRETA, FASES, PERDA_OURO_NA_MORTE, ULTIMA_FASE
from testes.apoio import entradas, monstro_de_teste, novo_jogador


class TestDadosDasFases(unittest.TestCase):
    def test_cinco_fases_e_uma_secreta(self):
        self.assertEqual(ULTIMA_FASE, 5)
        self.assertEqual(FASE_SECRETA, 6)
        self.assertEqual(sorted(FASES), [1, 2, 3, 4, 5, 6])

    def test_cada_fase_principal_tem_monstro_e_chefe(self):
        for numero in range(1, ULTIMA_FASE + 1):
            self.assertIn("mob", FASES[numero])
            self.assertIn("boss", FASES[numero])

    def test_fase_secreta_so_tem_o_chefe_opcional(self):
        self.assertNotIn("mob", FASES[FASE_SECRETA])
        self.assertIn("boss", FASES[FASE_SECRETA])

    def test_chefe_e_mais_forte_que_o_monstro_da_fase(self):
        for numero in range(1, ULTIMA_FASE + 1):
            mob, boss = FASES[numero]["mob"], FASES[numero]["boss"]
            for campo in ("vida", "dano", "exp", "ouro"):
                self.assertGreater(boss[campo], mob[campo], (numero, campo))

    def test_dificuldade_cresce_de_fase_para_fase(self):
        for numero in range(1, ULTIMA_FASE):
            for etapa in ("mob", "boss"):
                atual, proxima = FASES[numero][etapa], FASES[numero + 1][etapa]
                self.assertGreater(proxima["vida"], atual["vida"])
                self.assertGreater(proxima["dano"], atual["dano"])

    def test_chefe_secreto_e_o_mais_forte_do_jogo(self):
        secreto = FASES[FASE_SECRETA]["boss"]
        for numero in range(1, ULTIMA_FASE + 1):
            self.assertGreater(secreto["vida"], FASES[numero]["boss"]["vida"])
            self.assertGreater(secreto["dano"], FASES[numero]["boss"]["dano"])

    def test_cada_fase_tem_nome_ambiente_e_evento_proprios(self):
        nomes = [fase["nome"] for fase in FASES.values()]
        eventos = [fase["evento"]["nome"] for fase in FASES.values()]
        self.assertEqual(len(set(nomes)), 6)
        self.assertEqual(len(set(eventos)), 6)

    def test_cada_monstro_tem_nome_e_especial_proprios(self):
        monstros = [fase[etapa] for fase in FASES.values() for etapa in ("mob", "boss") if etapa in fase]
        self.assertEqual(len({m["nome"] for m in monstros}), len(monstros))
        self.assertEqual(len({m["especial"]["nome"] for m in monstros}), len(monstros))

    def test_temas_pedidos(self):
        self.assertEqual(FASES[1]["mob"]["nome"], "Lobo")
        self.assertIn("Lava", FASES[3]["evento"]["nome"])
        self.assertIn("Deserto", FASES[2]["nome"])
        self.assertIn("Vulcão", FASES[3]["nome"])

    def test_evento_tem_chance_e_dano_validos(self):
        for fase in FASES.values():
            self.assertTrue(0 < fase["evento"]["chance"] <= 100)
            self.assertGreater(fase["evento"]["dano"], 0)


class TestRecompensa(unittest.TestCase):
    def test_vitoria_da_exp_ouro_e_uma_pocao(self):
        jogador = novo_jogador("1")
        monstro = monstro_de_teste(exp=5, ouro=40)
        with entradas():
            main.receber_recompensa(jogador, monstro)
        self.assertEqual(jogador["exp"], 5)
        self.assertEqual(jogador["ouro"], 40)
        self.assertEqual(jogador["pocoes_vida"], 3)

    def test_recompensa_pode_subir_de_nivel(self):
        jogador = novo_jogador("1")
        with entradas() as saida:
            main.receber_recompensa(jogador, monstro_de_teste(exp=50))
        self.assertGreater(jogador["level"], 1)
        self.assertIn("Subiu para o level", saida.getvalue())


class TestJogarFase(unittest.TestCase):
    def jogar(self, jogador, resultados, numero=1, **argumentos):
        with patch.object(main, "batalhar", side_effect=resultados) as batalha, \
                patch.object(main, "loja"), patch.object(main, "abrir_bau") as bau, \
                patch.object(main, "salvar_jogo"), entradas() as saida:
            resultado = main.jogar_fase(jogador, numero, **argumentos)
        return resultado, batalha, bau, saida.getvalue()

    def test_fase_tem_monstro_depois_chefe(self):
        resultado, batalha, _, _ = self.jogar(novo_jogador("1"), ["vitoria", "vitoria"])
        nomes = [chamada.args[1]["nome"] for chamada in batalha.call_args_list]
        self.assertEqual(nomes, ["Lobo", "Lobo Alfa"])
        self.assertEqual(resultado, "vitoria")

    def test_bau_so_aparece_depois_do_chefe(self):
        _, _, bau, _ = self.jogar(novo_jogador("1"), ["vitoria", "vitoria"])
        bau.assert_called_once()

    def test_sem_vencer_o_chefe_nao_ha_bau(self):
        resultado, _, bau, _ = self.jogar(novo_jogador("1"), ["vitoria", "derrota"])
        self.assertEqual(resultado, "derrota")
        bau.assert_not_called()

    def test_fase_secreta_tem_so_uma_luta(self):
        _, batalha, bau, _ = self.jogar(novo_jogador("1"), ["vitoria"], numero=FASE_SECRETA)
        self.assertEqual(batalha.call_count, 1)
        bau.assert_called_once()

    def test_morrer_tira_parte_do_ouro_e_restaura_o_jogador(self):
        jogador = novo_jogador("1")
        jogador["ouro"] = 200
        jogador["vida"], jogador["efeitos"] = 0, {"veneno": 2}
        _, _, _, saida = self.jogar(jogador, ["derrota"])
        self.assertEqual(jogador["ouro"], 200 - 200 * PERDA_OURO_NA_MORTE // 100)
        self.assertEqual(jogador["vida"], jogador["vida_max"])
        self.assertEqual(jogador["efeitos"], {})
        self.assertIn("VOCÊ MORREU", saida)

    def test_morrer_sem_ouro_nao_deixa_ouro_negativo(self):
        jogador = novo_jogador("1")
        self.jogar(jogador, ["derrota"])
        self.assertEqual(jogador["ouro"], 0)

    def test_vitoria_restaura_vida_e_mana(self):
        jogador = novo_jogador("1")
        jogador["vida"], jogador["mana"] = 1, 0
        self.jogar(jogador, ["vitoria", "vitoria"])
        self.assertEqual(jogador["vida"], jogador["vida_max"])
        self.assertEqual(jogador["mana"], jogador["mana_max"])

    def test_salvar_e_sair_interrompe_a_fase(self):
        resultado, batalha, bau, _ = self.jogar(novo_jogador("1"), ["salvou"])
        self.assertEqual(resultado, "salvou")
        self.assertEqual(batalha.call_count, 1)
        bau.assert_not_called()

    def test_retomar_no_chefe_usa_o_monstro_salvo(self):
        monstro = monstro_de_teste(nome="Lobo Alfa", vida=33)
        _, batalha, _, _ = self.jogar(novo_jogador("1"), ["vitoria"], etapa_inicial="boss", monstro=monstro)
        self.assertEqual(batalha.call_count, 1)
        self.assertEqual(batalha.call_args.args[1]["vida"], 33)

    def test_monstro_sempre_nasce_com_a_vida_cheia(self):
        _, batalha, _, _ = self.jogar(novo_jogador("1"), ["vitoria", "vitoria"])
        for chamada in batalha.call_args_list:
            self.assertEqual(chamada.args[1]["vida"], chamada.args[1]["vida_max"])

    def test_modelo_da_fase_nao_e_alterado_pela_luta(self):
        modelo = FASES[1]["mob"]["vida"]
        monstro = main.criar_monstro(FASES[1]["mob"])
        monstro["vida"] = 1
        self.assertEqual(FASES[1]["mob"]["vida"], modelo)


class TestProgressao(unittest.TestCase):
    def processar(self, jogador, numero, resultado):
        with patch.object(main, "jogar_fase", return_value=resultado), \
                patch.object(main, "salvar_jogo"), entradas() as saida:
            sair = main.processar_fase(jogador, numero)
        return sair, saida.getvalue()

    def test_vencer_a_fase_atual_libera_a_proxima(self):
        jogador = novo_jogador("1")
        _, saida = self.processar(jogador, 1, "vitoria")
        self.assertEqual(jogador["fase"], 2)
        self.assertIn("Nova fase liberada", saida)

    def test_refazer_uma_fase_antiga_nao_avanca(self):
        jogador = novo_jogador("1")
        jogador["fase"] = 3
        self.processar(jogador, 1, "vitoria")
        self.assertEqual(jogador["fase"], 3)

    def test_derrota_nao_libera_fase(self):
        jogador = novo_jogador("1")
        self.processar(jogador, 1, "derrota")
        self.assertEqual(jogador["fase"], 1)

    def test_salvar_e_sair_encerra_o_jogo(self):
        sair, _ = self.processar(novo_jogador("1"), 1, "salvou")
        self.assertTrue(sair)

    def test_zerar_o_jogo_libera_a_fase_secreta_e_registra_os_turnos(self):
        jogador = novo_jogador("1")
        jogador["fase"] = 5
        jogador["stats"]["turnos"] = 123
        _, saida = self.processar(jogador, 5, "vitoria")
        self.assertEqual(jogador["fase"], FASE_SECRETA)
        self.assertEqual(jogador["zerou_em"], 123)
        self.assertIn("Fim de jogo", saida)
        self.assertIn("Fase secreta liberada", saida)
        self.assertIn("Resumo", saida)

    def test_zerar_de_novo_nao_troca_o_recorde(self):
        jogador = novo_jogador("1")
        jogador["fase"] = FASE_SECRETA
        jogador["zerou_em"] = 100
        jogador["stats"]["turnos"] = 400
        _, saida = self.processar(jogador, 5, "vitoria")
        self.assertEqual(jogador["zerou_em"], 100)
        self.assertNotIn("Fim de jogo", saida)

    def test_vencer_o_chefe_secreto_nao_muda_nada(self):
        jogador = novo_jogador("1")
        jogador["fase"] = FASE_SECRETA
        jogador["zerou_em"] = 100
        self.processar(jogador, FASE_SECRETA, "vitoria")
        self.assertEqual(jogador["fase"], FASE_SECRETA)
        self.assertEqual(jogador["zerou_em"], 100)


class TestMapa(unittest.TestCase):
    def mapa(self, jogador, *respostas):
        with entradas(*respostas) as saida:
            escolha = main.menu_mapa(jogador)
        return escolha, saida.getvalue()

    def test_so_lista_as_fases_liberadas(self):
        jogador = novo_jogador("1")
        jogador["fase"] = 2
        escolha, saida = self.mapa(jogador, "1")
        self.assertIn("[1] Floresta Sombria", saida)
        self.assertIn("[2] Deserto Escaldante", saida)
        self.assertNotIn("[3]", saida)

    def test_nao_deixa_entrar_numa_fase_bloqueada(self):
        escolha, saida = self.mapa(novo_jogador("1"), "2", "1")
        self.assertEqual(escolha, 1)
        self.assertIn("Opção inválida", saida)

    def test_pode_refazer_qualquer_fase_liberada(self):
        jogador = novo_jogador("1")
        jogador["fase"] = 4
        escolha, _ = self.mapa(jogador, "2")
        self.assertEqual(escolha, 2)

    def test_fase_secreta_aparece_marcada_como_opcional(self):
        jogador = novo_jogador("1")
        jogador["fase"] = FASE_SECRETA
        _, saida = self.mapa(jogador, "0")
        self.assertIn("Abismo Esquecido (secreta, chefe opcional)", saida)

    def test_equipamentos_e_sair(self):
        escolha, saida = self.mapa(novo_jogador("1"), "e", "0")
        self.assertIsNone(escolha)
        self.assertIn("Espada: vazio", saida)


if __name__ == "__main__":
    unittest.main()
