# Jogo RPG

Um RPG de batalha por turnos que roda no terminal, feito em Python. Fiz esse projeto para praticar o que estou aprendendo: dicionários, funções, loops, arquivos JSON e testes.

## Como rodar

Precisa ter o Python 3 instalado.

```
python main.py
```

No Windows, se não funcionar, use `py main.py`. No Linux e no Mac, use `python3 main.py`.

## Como jogar

Você escolhe uma classe (Guerreiro, Mago ou Arqueiro) e passa por 5 fases. Cada fase tem um monstro e um chefe. Depois de cada vitória abre uma loja, e o chefe deixa um baú com um equipamento. As fases podem ser refeitas para ganhar ouro, experiência e equipamentos melhores.

Ações durante a luta:

- Atacar: causa dano, com 10% de chance de crítico (dano dobrado) e 10% de chance de errar
- Especial: gasta 10 de mana e nunca erra
- Defender: reduz pela metade o próximo golpe e bloqueia os status
- Poção de vida: recupera 50 de vida
- Poção de mana: recupera 30 de mana
- Salvar e sair: guarda a luta exatamente no ponto em que está

O jogo é difícil de propósito, inspirado em jogos do tipo Souls. O monstro avisa um turno antes de usar o golpe especial, e é nessa hora que vale a pena defender. Se o jogador morre, perde 25% do ouro. Mesmo assim dá para vencer: testei com um bot que joga sozinho.

## Fases

| Fase | Monstro | Chefe | Evento |
| --- | --- | --- | --- |
| Floresta Sombria | Lobo | Lobo Alfa | Galho despenca |
| Deserto Escaldante | Escorpião Gigante | Esfinge de Areia | Tempestade de areia |
| Vulcão Ardente | Golem de Lava | Dragão de Magma | Lava cai do teto |
| Cripta Esquecida | Esqueleto Guerreiro | Lorde Necromante | Ossos desabam |
| Montanha Gelada | Yeti | Dragão de Gelo | Avalanche |

O evento da fase pode cair no jogador ou no monstro. Os golpes especiais podem causar status (sangramento, veneno, queimadura, maldição e hipotermia). Cada status causa dano por 3 turnos e vários podem ficar ativos juntos.

Ao zerar o jogo, abre o Abismo Esquecido, uma fase secreta com um chefe opcional.

## Equipamentos

O chefe solta um equipamento aleatório: espada, escudo, cajado ou arco. Cada um tem um tier de 1 a 3, e o nível é sorteado dentro da faixa do tier:

- Tier 1: nível 7 a 22
- Tier 2: nível 23 a 40
- Tier 3: nível 41 a 60

O que cada tipo faz:

- Espada: soma metade do nível no ataque normal
- Escudo: reduz o dano recebido em nível dividido por 3
- Cajado: soma o nível no ataque especial
- Arco: aumenta a chance de crítico em metade do nível (%)

Equipamentos de tier 2 e 3 têm um efeito extra, que vale 10% vezes o tier: a espada rouba vida, o escudo devolve parte do dano, o cajado pode atordoar o monstro e o arco pode atirar duas flechas.

A loja de cada fase vende duas armas diferentes, com preços entre 380 e 2400 de ouro. Como o ouro das lutas é pouco, é preciso refazer fases para juntar.

## Saves e ranking

Cada jogador tem um arquivo na pasta `saves/`. No menu inicial dá para continuar um jogo, começar outro (o jogo pergunta antes de sobrescrever um nome que já existe) e apagar um save. Arquivos corrompidos ou de versões antigas são ignorados.

O ranking mostra quem zerou o jogo, ordenado pelo menor número de turnos.

## Testes

```
python -m unittest
```

A pasta `testes/` tem quase 200 testes com `unittest`. Tem testes pequenos para cada regra (crítico, defesa, status, loja, save...) e também partidas completas jogadas por um bot, para conferir que o jogo é difícil mas dá para vencer sem comprar nada na loja.

## Estrutura

```
main.py    funções do jogo
dados.py   tabelas: classes, fases, monstros, equipamentos, status e loja
testes/    testes automáticos
saves/     criada sozinha quando o jogo salva
```

Deixei as tabelas em `dados.py` para poder mudar um preço ou criar uma fase sem mexer nas funções do `main.py`.

## Bugs que apareceram no caminho

- **Nível só subia com experiência exata.** O código original usava `==`, então se o jogador passasse da experiência necessária nunca subia de nível. Troquei por `>=` e o que sobra de experiência é guardado. Também funciona quando sobe mais de um nível de uma vez.
- **Vida não enchia depois de subir de nível.** Eu restaurava a vida antes de aplicar o aumento de nível, então aparecia algo como 120/140. Descobri com um teste e agora a restauração acontece depois.
- **O monstro era criado duas vezes.** Isso fazia a vida dele ser sorteada de novo no meio da fase. Passei a criar uma vez só por luta.
- **O save aparecia em lugares diferentes.** O caminho dependia da pasta em que o terminal estava aberto. Agora a pasta `saves/` fica sempre ao lado do `main.py`.
- **Save quebrado ou antigo travava o jogo.** Usei `try/except` na leitura e conferi se o arquivo tem as chaves necessárias antes de mostrar na lista.
- **Um teste achava emojis nos próprios arquivos.** O teste que garante que não há emoji no projeto tinha emojis escritos no código dele. Troquei por intervalos escritos em código unicode.

## O que aprendi

- Usar dicionários para guardar o jogador e os monstros, o que deixa fácil salvar tudo em JSON
- Dividir o jogo em funções pequenas
- Controlar o fim da luta com `while`
- Ler e gravar arquivos JSON e tratar erros com `try/except`
- Escrever testes com `unittest` e simular o `input()` para jogar automaticamente

## Créditos e uso de IA

Usei como base o vídeo do Progamador Python: https://www.youtube.com/watch?v=CS_Th38ADug&list=PL0UvQ8QfB92wZWh2NVVHmUSGu_Bdy_Ehl&index=3

Também usei IA (Claude, da Anthropic) como ajuda: para encontrar e corrigir bugs, para sugerir ideias de mecânicas e para montar os testes. A estrutura do código eu entendo e consigo explicar, mas deixo aqui registrado que a IA participou do projeto.
