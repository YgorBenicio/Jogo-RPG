# Jogo RPG

Um jogo de RPG por turnos feito em Python que roda direto no terminal. Fiz esse projeto para praticar o que estou aprendendo em programação, como dicionários, funções, loops, arquivos JSON e testes automatizados.

## Como rodar

Precisa ter o Python 3 instalado.

```
python main.py
```

No Windows, se não funcionar, use `py main.py`. No Linux e no Mac, tente `python3 main.py`.

## Como jogar

Você escolhe uma classe (Guerreiro, Mago ou Arqueiro) e precisa passar por 5 fases. Cada fase tem um monstro e um chefe. Depois das vitórias, abre uma loja para comprar equipamentos, e os chefes deixam baús com equipamentos aleatórios. Também dá para repetir as fases para conseguir mais ouro, experiência e equipamentos melhores.

Durante as lutas, você pode:

- **Atacar:** causa dano normal, com 10% de chance de crítico (dano dobrado) e 10% de chance de errar.
- **Especial:** gasta 10 de mana e não erra.
- **Defender:** reduz pela metade o próximo golpe recebido e bloqueia efeitos de status.
- **Poção de vida:** recupera 50 de vida.
- **Poção de mana:** recupera 30 de mana.
- **Salvar e sair:** salva a partida para continuar depois, até mesmo durante uma luta.

Tentei deixar o jogo difícil de propósito, com inspiração em jogos do estilo Souls. Os monstros avisam um turno antes de usar seus golpes especiais, então é importante prestar atenção e saber a hora de defender. Se o jogador morrer, perde 25% do ouro.

Também fiz testes com um bot jogando sozinho para conferir se dava para terminar o jogo sem precisar comprar equipamentos na loja.

## Fases

| Fase | Monstro | Chefe | Evento |
| --- | --- | --- | --- |
| Floresta Sombria | Lobo | Lobo Alfa | Galho despenca |
| Deserto Escaldante | Escorpião Gigante | Esfinge de Areia | Tempestade de areia |
| Vulcão Ardente | Golem de Lava | Dragão de Magma | Lava cai do teto |
| Cripta Esquecida | Esqueleto Guerreiro | Lorde Necromante | Ossos desabam |
| Montanha Gelada | Yeti | Dragão de Gelo | Avalanche |

Os eventos podem atingir tanto o jogador quanto o monstro. Os golpes especiais também podem causar efeitos como sangramento, veneno, queimadura, maldição e hipotermia. Cada efeito causa dano por 3 turnos, e vários podem ficar ativos ao mesmo tempo.

Depois de zerar o jogo, é desbloqueado o Abismo Esquecido, uma fase secreta com um chefe opcional.

## Equipamentos

Os chefes deixam um equipamento aleatório: espada, escudo, cajado ou arco. Cada equipamento tem um tier de 1 a 3, e seu nível é sorteado dentro da faixa correspondente:

- Tier 1: nível 7 a 22
- Tier 2: nível 23 a 40
- Tier 3: nível 41 a 60

Cada tipo de equipamento tem uma função diferente:

- **Espada:** aumenta o ataque normal em metade do nível do equipamento.
- **Escudo:** reduz o dano recebido de acordo com o nível dividido por 3.
- **Cajado:** aumenta o dano do ataque especial de acordo com o nível.
- **Arco:** aumenta a chance de crítico em metade do nível, em porcentagem.

Os equipamentos de tier 2 e 3 também têm efeitos extras. A espada pode roubar vida, o escudo pode devolver parte do dano recebido, o cajado pode atordoar o monstro e o arco pode disparar duas flechas. A chance ou o valor do efeito depende do tier, usando a proporção de 10% por tier.

A loja de cada fase vende duas armas diferentes, com preços entre 380 e 2400 de ouro. Como não é tão fácil conseguir ouro nas lutas, às vezes é preciso repetir algumas fases para juntar dinheiro.

## Saves e ranking

Cada jogador tem um arquivo de save na pasta `saves/`. No menu inicial, dá para continuar uma partida, começar outra ou apagar um save. Se o nome escolhido já existir, o jogo pergunta antes de sobrescrever o arquivo.

Também fiz algumas verificações para evitar problemas com saves corrompidos ou de versões antigas. Esses arquivos são ignorados para evitar que o jogo trave.

O ranking mostra quem conseguiu zerar o jogo, organizado pelo menor número de turnos utilizados.

## Testes

Para executar os testes, use:

```
python -m unittest
```

A pasta `testes/` tem quase 200 testes feitos com `unittest`. Tem testes para várias regras do jogo, como crítico, defesa, efeitos de status, loja e saves. Também fiz testes de partidas completas com um bot jogando sozinho, para conferir se dava para vencer sem comprar nada na loja.

## Estrutura

```
main.py    funções principais do jogo
dados.py   dados das classes, fases, monstros, equipamentos, status e loja
testes/    testes automatizados
saves/     criada automaticamente quando o jogo salva
```

Deixei os dados separados no `dados.py` para facilitar as mudanças. Assim, se eu quiser alterar um preço ou criar uma fase nova, por exemplo, não preciso mexer diretamente nas funções do `main.py`.

## Bugs que apareceram no caminho

Durante o desenvolvimento, encontrei alguns problemas que não tinha percebido no começo. Fui corrigindo conforme testava o jogo e encontrava situações que não funcionavam como eu esperava.

- **O personagem não subia de nível em algumas situações.** No começo, eu usava `==` para verificar se o jogador tinha a experiência necessária. O problema era que, se ele ganhasse mais experiência do que precisava, não subia de nível. Troquei por `>=` e também fiz com que a experiência que sobrasse fosse mantida. Assim, o jogador consegue subir mais de um nível de uma vez.
- **A vida não ficava cheia depois de subir de nível.** Percebi isso durante os testes, quando o personagem aumentava a vida máxima, mas continuava com a quantidade antiga de vida. O problema era a ordem em que eu fazia as coisas. Mudei o código para restaurar a vida depois de aplicar o aumento de nível.
- **O monstro acabava sendo criado duas vezes.** Era uma criação repetida no código, o que podia deixar a luta com um monstro diferente do que estava sendo mostrado. Depois de encontrar o problema, ajustei o código para criar o monstro apenas uma vez por luta.
- **Os saves eram salvos em lugares diferentes.** Quando eu executava o jogo a partir de outra pasta, os arquivos podiam acabar no lugar errado. Corrigi o caminho para que a pasta `saves/` fique sempre ao lado do `main.py`, independentemente de onde o terminal foi aberto.
- **Um save com problemas podia atrapalhar o início do jogo.** Percebi que um arquivo corrompido ou de uma versão antiga podia causar erros na hora de carregar a lista de partidas. Adicionei `try/except` e verificações para ignorar arquivos que não tivessem as informações necessárias.

Esses problemas me ajudaram a perceber que nem sempre o código funciona como a gente espera na primeira tentativa. Por isso, fui criando testes para conferir as correções e evitar que os mesmos erros aparecessem novamente.

## O que aprendi

Com esse projeto, consegui praticar várias coisas que estava aprendendo em Python:

- Usar dicionários para guardar as informações do jogador e dos monstros e facilitar o salvamento em JSON.
- Dividir o código em funções menores para organizar melhor o projeto.
- Usar loops `while` para controlar o funcionamento das batalhas.
- Ler e gravar arquivos JSON e tratar erros com `try/except`.
- Criar testes com `unittest`.
- Simular o `input()` para testar as partidas automaticamente.
- Encontrar e corrigir bugs durante o desenvolvimento.

Também percebi que os testes ajudam bastante, porque alguns problemas não aparecem durante uma partida normal, mas podem ser encontrados ao simular situações diferentes.

## Créditos e uso de IA

Usei como referência o vídeo do Programador Python:

https://www.youtube.com/watch?v=CS_Th38ADug&list=PL0UvQ8QfB92wZWh2NVVHmUSGu_Bdy_Ehl&index=3

Também usei o Claude, da Anthropic, como ajuda durante o desenvolvimento, principalmente para encontrar e corrigir bugs, pensar em algumas mecânicas e montar os testes.

A IA fez parte do desenvolvimento, mas procurei entender como o código funciona e as soluções utilizadas, para conseguir explicar o projeto.
