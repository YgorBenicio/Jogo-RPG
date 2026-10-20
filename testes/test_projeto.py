import os
import re
import tokenize
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMOJIS = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50]")


def arquivos(extensao):
    for pasta, subpastas, nomes in os.walk(RAIZ):
        subpastas[:] = [p for p in subpastas if p not in ("__pycache__", "saves", ".git")]
        for nome in nomes:
            if nome.endswith(extensao):
                yield os.path.join(pasta, nome)


def ler(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        return arquivo.read()


class TestEstruturaDoRepositorio(unittest.TestCase):
    def test_arquivos_principais_ficam_na_raiz(self):
        for nome in ("main.py", "dados.py", "README.md", ".gitignore"):
            self.assertTrue(os.path.isfile(os.path.join(RAIZ, nome)), nome)

    def test_existe_a_pasta_de_testes(self):
        self.assertTrue(os.path.isdir(os.path.join(RAIZ, "testes")))

    def test_pastas_antigas_nao_existem_mais(self):
        for nome in ("Jogo", "rpg", "tests", ".github", "gitignore", "save.json"):
            self.assertFalse(os.path.exists(os.path.join(RAIZ, nome)), nome)

    def test_gitignore_ignora_saves_e_cache(self):
        linhas = ler(os.path.join(RAIZ, ".gitignore")).split()
        self.assertIn("saves/", linhas)
        self.assertIn("__pycache__/", linhas)


class TestEstiloDoCodigo(unittest.TestCase):
    def test_nenhum_emoji_no_projeto(self):
        for extensao in (".py", ".md"):
            for caminho in arquivos(extensao):
                self.assertIsNone(EMOJIS.search(ler(caminho)), caminho)

    def test_nenhum_comentario_nos_arquivos_python(self):
        for caminho in arquivos(".py"):
            with open(caminho, "rb") as arquivo:
                comentarios = [t.string for t in tokenize.tokenize(arquivo.readline)
                               if t.type == tokenize.COMMENT]
            self.assertEqual(comentarios, [], caminho)

    def test_main_so_roda_quando_executado_diretamente(self):
        self.assertIn('if __name__ == "__main__":', ler(os.path.join(RAIZ, "main.py")))

    def test_readme_explica_como_executar_e_testar(self):
        readme = ler(os.path.join(RAIZ, "README.md"))
        self.assertIn("python main.py", readme)
        self.assertIn("python -m unittest", readme)


if __name__ == "__main__":
    unittest.main()
