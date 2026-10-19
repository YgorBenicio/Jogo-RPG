# Jogo RPG

RPG de batalha por turnos para o terminal, feito em Python sem bibliotecas externas.

## Como executar

Requer Python 3.8 ou superior.

```
python main.py
```

No Windows, use `py main.py`. No Linux e no macOS, use `python3 main.py`.

## Como jogar

O jogador escolhe uma classe (Guerreiro, Mago ou Arqueiro) e percorre cinco fases. Cada fase tem um monstro comum e um chefe. Depois de cada vitória, o jogo abre uma loja. Ao derrotar o chefe, o jogador recebe um baú com um equipamento.

Fases já concluídas podem ser refeitas para ganhar experiência, ouro e novos baús.

| Ação | Efeito |
| --- | --- |
| Atacar | Dano aleatório com 10% de chance de acerto crítico (dano dobrado) e 10% de chance de errar |
| Especial | Custa 10 de mana, nunca erra e causa mais dano que o ataque normal |
| Defender | Reduz pela metade o dano do próximo ataque do monstro |
| Poção de vida | Recupera 50 de vida |
| Poção de mana | Recupera 30 de mana |
| Salvar e sair | Grava a luta no ponto exato em que está |

## Fases

| Fase | Monstro | Chefe | Evento do ambiente | Efeito de status |
| --- | --- | --- | --- | --- |
| Floresta Sombria | Lobo | Lobo Alfa | Galho despenca | Sangramento |
| Deserto Escaldante | Escorpião Gigante | Esfinge de Areia | Tempestade de areia | Veneno |
| Vulcão Ardente | Golem de Lava | Dragão de Magma | Lava cai do teto | Queimadura |
| Cripta Esquecida | Esqueleto Guerreiro | Lorde Necromante | Ossos desabam | Maldição |
| Montanha Gelada | Yeti | Dragão de Gelo | Avalanche | Hipotermia |

A cada rodada pode ocorrer um evento do ambiente, que atinge o jogador ou o monstro ao acaso. Cada monstro tem um golpe especial com chance de aplicar um efeito de status, que causa dano por três turnos.

## Equipamentos

Os chefes soltam um equipamento de tipo aleatório. Cada item tem um tier (1 a 3) e um nível sorteado dentro da faixa do tier. Fases mais avançadas aumentam a chance de tiers maiores.

| Tier | Faixa de nível |
| --- | --- |
| 1 | 7 a 22 |
| 2 | 23 a 40 |
| 3 | 41 a 60 |

| Tipo | Efeito |
| --- | --- |
| Espada | Dano do ataque normal + nível / 2 |
| Escudo | Dano recebido - nível / 3 |
| Cajado | Dano do ataque especial + nível |
| Arco | Chance de crítico + nível / 2 (%) |

A loja de cada fase vende dois equipamentos exclusivos, com preços altos que incentivam refazer fases para juntar ouro.

## Salvamento

Cada jogador tem um arquivo próprio na pasta `saves/`. No menu inicial é possível continuar um save, criar um novo (com confirmação antes de sobrescrever um nome existente) e apagar um save. Arquivos corrompidos ou em formato antigo são ignorados.

## Estrutura

```
main.py    lógica do jogo
dados.py   tabelas: classes, fases, monstros, equipamentos, efeitos e loja
saves/     criada automaticamente
```

Os valores de balanceamento ficam em `dados.py`, então alterar um preço, um monstro ou uma fase não exige mexer na lógica.

## Decisões de projeto

- Jogador e monstros são dicionários, o que permite salvar o estado direto em JSON.
- O estado de uma luta em andamento é gravado junto com o jogador, permitindo retomar do mesmo ponto.
- A dificuldade foi ajustada com simulações automáticas de partidas, garantindo que as três classes consigam concluir o jogo apenas com os baús dos chefes.
