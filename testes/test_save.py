import json
import os
import unittest
from unittest.mock import patch

import main
from testes.apoio import entradas, monstro_de_teste, novo_jogador, pasta_temporaria


class TestNomeDoArquivo(unittest.TestCase):
    def test_nome_com_simbolos_vira_arquivo_seguro(self):
        with pasta_temporaria():
            caminho = main.caminho_save("Ygor / ../Bena!")
        self.assertEqual(os.path.basename(caminho), "ygorbena.json")

    def test_nome_sem_letras_usa_nome_padrao(self):
        with pasta_temporaria():
            self.assertTrue(main.caminho_save("!!!").endswith("heroi.json"))

    def test_maiusculas_e_minusculas_dao_o_mesmo_arquivo(self):
        with pasta_temporaria():
            self.assertEqual(main.caminho_save("Ana"), main.caminho_save("ANA"))


class TestSalvarECarregar(unittest.TestCase):
    def test_salvar_e_listar_recupera_o_jogador(self):
        with pasta_temporaria():
            jogador = novo_jogador("2", "Maria")
            jogador["ouro"] = 321
            jogador["equipamentos"]["Arco"] = {"nome": "Arco", "tipo": "Arco", "tier": 2, "nivel": 30}
            main.salvar_jogo(jogador, None)
            saves = main.listar_saves()
        self.assertEqual(len(saves), 1)
        carregado = saves[0][1]["jogador"]
        self.assertEqual(carregado, jogador)
        self.assertIsNone(saves[0][1]["batalha"])

    def test_cada_jogador_tem_o_seu_arquivo(self):
        with pasta_temporaria() as pasta:
            main.salvar_jogo(novo_jogador("1", "Ana"), None)
            main.salvar_jogo(novo_jogador("2", "Bia"), None)
            main.salvar_jogo(novo_jogador("3", "Caio"), None)
            self.assertEqual(sorted(os.listdir(pasta)), ["ana.json", "bia.json", "caio.json"])

    def test_pasta_de_saves_e_criada_automaticamente(self):
        with pasta_temporaria() as pasta:
            os.rmdir(pasta)
            main.salvar_jogo(novo_jogador("1", "Ana"), None)
            self.assertTrue(os.path.isdir(pasta))

    def test_pasta_de_saves_fica_ao_lado_do_main(self):
        raiz = os.path.dirname(os.path.abspath(main.__file__))
        self.assertEqual(main.PASTA_SAVES, os.path.join(raiz, "saves"))

    def test_acentos_sobrevivem_ao_salvar(self):
        with pasta_temporaria():
            main.salvar_jogo(novo_jogador("1", "José"), None)
            self.assertEqual(main.listar_saves()[0][1]["jogador"]["nome"], "José")

    def test_sem_pasta_nao_ha_saves(self):
        with patch.object(main, "PASTA_SAVES", "/caminho/que/nao/existe"):
            self.assertEqual(main.listar_saves(), [])

    def test_save_corrompido_e_ignorado(self):
        with pasta_temporaria() as pasta:
            main.salvar_jogo(novo_jogador("1", "Ana"), None)
            with open(os.path.join(pasta, "lixo.json"), "w") as arquivo:
                arquivo.write("{ isto nao e json")
            self.assertEqual(len(main.listar_saves()), 1)

    def test_save_de_versao_antiga_e_ignorado(self):
        with pasta_temporaria() as pasta:
            with open(os.path.join(pasta, "velho.json"), "w") as arquivo:
                json.dump({"jogador": {"nome": "Velho", "level": 2}, "proximo": 3}, arquivo)
            self.assertEqual(main.listar_saves(), [])

    def test_arquivos_que_nao_sao_json_sao_ignorados(self):
        with pasta_temporaria() as pasta:
            with open(os.path.join(pasta, "notas.txt"), "w") as arquivo:
                arquivo.write("oi")
            self.assertEqual(main.listar_saves(), [])


class TestSaveNoMeioDaLuta(unittest.TestCase):
    def test_continuar_devolve_a_luta_no_ponto_exato(self):
        with pasta_temporaria():
            jogador = novo_jogador("1", "Luta")
            jogador["vida"] = 55
            monstro = monstro_de_teste(vida=44, preparando=True)
            main.salvar_jogo(jogador, {"fase": 3, "etapa": "boss", "monstro": monstro})
            with entradas("2", "1"):
                carregado, batalha = main.menu_inicial()
        self.assertEqual(carregado["vida"], 55)
        self.assertEqual(batalha["fase"], 3)
        self.assertEqual(batalha["etapa"], "boss")
        self.assertEqual(batalha["monstro"]["vida"], 44)
        self.assertTrue(batalha["monstro"]["preparando"])

    def test_iniciar_jogo_retoma_a_luta_salva(self):
        with pasta_temporaria():
            monstro = monstro_de_teste(nome="Dragão de Magma", vida=44)
            main.salvar_jogo(novo_jogador("1", "Luta"), {"fase": 3, "etapa": "boss", "monstro": monstro})
            with entradas("2", "1"), patch.object(main, "batalhar", return_value="salvou") as batalha:
                main.iniciar_jogo()
        args = batalha.call_args.args
        self.assertEqual((args[2], args[3]), (3, "boss"))
        self.assertEqual(args[1]["vida"], 44)

    def test_save_depois_da_luta_nao_guarda_monstro(self):
        with pasta_temporaria():
            main.salvar_jogo(novo_jogador("1", "Ana"), None)
            self.assertIsNone(main.listar_saves()[0][1]["batalha"])


class TestMenuDeSaves(unittest.TestCase):
    def test_continuar_lista_nome_classe_level_e_fase(self):
        with pasta_temporaria():
            jogador = novo_jogador("3", "Zeca")
            jogador["level"], jogador["fase"] = 4, 2
            main.salvar_jogo(jogador, None)
            with entradas("0") as saida:
                main.escolher_save("Continuar")
        texto = saida.getvalue()
        for trecho in ("Zeca", "Arqueiro", "Level 4", "Fase 2"):
            self.assertIn(trecho, texto)

    def test_sem_saves_avisa(self):
        with pasta_temporaria(), entradas() as saida:
            self.assertIsNone(main.escolher_save("Continuar"))
        self.assertIn("Nenhum save encontrado", saida.getvalue())

    def test_escolha_invalida_pergunta_de_novo(self):
        with pasta_temporaria():
            main.salvar_jogo(novo_jogador("1", "Ana"), None)
            with entradas("9", "x", "1") as saida:
                save = main.escolher_save("Continuar")
        self.assertEqual(save[1]["jogador"]["nome"], "Ana")
        self.assertEqual(saida.getvalue().count("Opção inválida"), 2)


class TestNovoJogo(unittest.TestCase):
    def test_cria_jogador_com_nome_e_classe(self):
        with entradas("Ana", "2"):
            jogador = main.novo_jogo()
        self.assertEqual((jogador["nome"], jogador["classe"]), ("Ana", "Mago"))

    def test_nome_vazio_vira_heroi(self):
        with entradas("   ", "1"):
            self.assertEqual(main.novo_jogo()["nome"], "Herói")

    def test_classe_invalida_pergunta_de_novo(self):
        with entradas("Ana", "9", "x", "3") as saida:
            jogador = main.novo_jogo()
        self.assertEqual(jogador["classe"], "Arqueiro")
        self.assertIn("Opção inválida", saida.getvalue())

    def test_nome_existente_pede_confirmacao_e_recusa(self):
        with pasta_temporaria():
            main.salvar_jogo(novo_jogador("1", "Ana"), None)
            with entradas("Ana", "n") as saida:
                self.assertIsNone(main.novo_jogo())
        self.assertIn("Sobrescrever", saida.getvalue())

    def test_nome_existente_sobrescreve_se_confirmar(self):
        with pasta_temporaria():
            main.salvar_jogo(novo_jogador("1", "Ana"), None)
            with entradas("Ana", "s", "2"):
                jogador = main.novo_jogo()
        self.assertEqual(jogador["classe"], "Mago")


class TestApagarSave(unittest.TestCase):
    def test_apagar_com_confirmacao(self):
        with pasta_temporaria() as pasta:
            main.salvar_jogo(novo_jogador("1", "Ana"), None)
            with entradas("1", "s") as saida:
                main.apagar_save()
            self.assertEqual(os.listdir(pasta), [])
        self.assertIn("Save apagado", saida.getvalue())

    def test_apagar_cancelado_mantem_o_arquivo(self):
        with pasta_temporaria() as pasta:
            main.salvar_jogo(novo_jogador("1", "Ana"), None)
            with entradas("1", "n"):
                main.apagar_save()
            self.assertEqual(os.listdir(pasta), ["ana.json"])

    def test_apagar_so_existe_no_menu_inicial(self):
        with entradas("0") as saida:
            main.menu_inicial()
        self.assertIn("Apagar save", saida.getvalue())
        with entradas("0") as saida:
            main.menu_mapa(novo_jogador("1"))
        self.assertNotIn("Apagar", saida.getvalue())

    def test_apagar_pelo_menu_inicial(self):
        with pasta_temporaria() as pasta:
            main.salvar_jogo(novo_jogador("1", "Ana"), None)
            with entradas("3", "1", "s", "0"):
                main.menu_inicial()
            self.assertEqual(os.listdir(pasta), [])


class TestMenuInicial(unittest.TestCase):
    def test_sair_encerra_sem_jogar(self):
        with entradas("0"), patch.object(main, "menu_mapa") as mapa:
            main.iniciar_jogo()
        mapa.assert_not_called()

    def test_opcao_invalida(self):
        with entradas("x", "0") as saida:
            main.menu_inicial()
        self.assertIn("Opção inválida", saida.getvalue())

    def test_sair_do_mapa_salva_e_mostra_o_resumo(self):
        with pasta_temporaria() as pasta, entradas("1", "Ana", "1", "0") as saida:
            main.iniciar_jogo()
            self.assertEqual(os.listdir(pasta), ["ana.json"])
        self.assertIn("Progresso salvo", saida.getvalue())
        self.assertIn("Resumo", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
