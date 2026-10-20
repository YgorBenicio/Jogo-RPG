# Jogo RPG

RPG de batalha por turnos para o terminal, feito em Python sem bibliotecas externas. O jogo tem dificuldade única, inspirada em jogos do estilo Souls: os golpes fortes dos monstros são avisados com um turno de antecedência, errar custa caro, mas todo chefe pode ser vencido.

## Como executar

Requer Python 3.8 ou superior.

```
python main.py
```

No Windows, use `py main.py`. No Linux e no macOS, use `python3 main.py`.

## Como jogar

O jogador escolhe uma classe (Guerreiro, Mago ou Arqueiro) e percorre cinco fases. Cada fase tem um monstro comum e um chefe. Depois de cada vitória o jogo abre uma loja, e o chefe deixa um baú com um equipamento. Fases concluídas podem ser refeitas para ganhar experiência, ouro e novos baús.

| Ação | Efeito |
| --- | --- |
| Atacar | Dano aleatório, com 10% de chance de crítico (dano dobrado) e 10% de chance de errar |
| Especial | Custa 10 de mana, nunca erra e causa mais dano que o ataque normal |
| Defender | Reduz pela metade o dano do próximo golpe e bloqueia os status do especial |
| Poção de vida | Recupera 50 de vida |
| Poção de mana | Recupera 30 de mana |
| Salvar e sair | Grava a luta no ponto exato em que está |

## Dificuldade

- O monstro avisa com um turno de antecedência que vai usar o especial. Esse é o momento de defender.
- Cada especial causa dano multiplicado e pode aplicar status. Os chefes aplicam mais de um status ao mesmo tempo.
- Morrer faz perder 25% do ouro.
- Ao subir de nível e ao fim de cada luta, vida e mana são restauradas.

## Fases

| Fase | Monstro | Chefe | Evento do ambiente |
| --- | --- | --- | --- |
| Floresta Sombria | Lobo | Lobo Alfa | Galho despenca |
| Deserto Escaldante | Escorpião Gigante | Esfinge de Areia | Tempestade de areia |
| Vulcão Ardente | Golem de Lava | Dragão de Magma | Lava cai do teto |
| Cripta Esquecida | Esqueleto Guerreiro | Lorde Necromante | Ossos desabam |
| Montanha Gelada | Yeti | Dragão de Gelo | Avalanche |

A cada rodada pode ocorrer um evento do ambiente, que atinge o jogador ou o monstro ao acaso.

Os status são Sangramento, Veneno, Queimadura, Maldição e Hipotermia. Cada um causa dano por três turnos, e vários podem estar ativos ao mesmo tempo.

Ao zerar o jogo, uma fase secreta é liberada: o Abismo Esquecido, com um único chefe opcional e o melhor equipamento do jogo.

## Equipamentos

Cada item tem um tier (1 a 3) e um nível sorteado dentro da faixa do tier. Fases mais avançadas aumentam a chance de tiers maiores.

| Tier | Faixa de nível |
| --- | --- |
| 1 | 7 a 22 |
| 2 | 23 a 40 |
| 3 | 41 a 60 |

| Tipo | Efeito | Efeito extra (tier 2 e 3) |
| --- | --- | --- |
| Espada | Dano do ataque normal + nível / 2 | Roubo de vida |
| Escudo | Dano recebido - nível / 3 | Reflexo de dano |
| Cajado | Dano do especial + nível | Chance de atordoar |
| Arco | Chance de crítico + nível / 2 (%) | Flecha dupla |

O efeito extra é 10% por tier. A loja de cada fase vende duas armas exclusivas, com preços altos.

## Salvamento e ranking

Cada jogador tem um arquivo próprio na pasta `saves/`. No menu inicial é possível continuar um save, criar um novo (com confirmação antes de sobrescrever) e apagar um save. Arquivos corrompidos ou de versões antigas são ignorados.

O ranking mostra os jogadores que zeraram o jogo, ordenados pelo menor número de turnos.

## Testes

```
python -m unittest
```

A pasta `testes/` cobre as regras do jogo, a loja, os saves, o ranking e a estrutura do projeto. Há também partidas completas jogadas por um bot, que verificam que o jogo é difícil mas pode ser vencido sem comprar nada na loja.

## Estrutura

```
main.py    lógica do jogo
dados.py   tabelas: classes, fases, monstros, equipamentos, efeitos e loja
testes/    testes automatizados
saves/     criada automaticamente
```

## Decisões de projeto

- Jogador e monstros são dicionários, o que permite salvar o estado direto em JSON.
- As tabelas ficam em `dados.py`, então alterar um preço, um monstro ou uma fase não exige mexer na lógica.
- A pasta de saves é resolvida a partir do local do `main.py`, e não do diretório em que o comando foi executado.
- A dificuldade foi calibrada com simulações de partidas completas, repetíveis por semente.
