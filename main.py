from random import randint
from random import choice

lista_npcs = []

# Definindo o dicionário do jogador. O dicionário contém informações sobre o jogador, como nome, nível, experiência e dano
player = {
    "nome": input("Digite o nome do jogador: "),
    "level": 1,
    "exp" : 0,
    "exp_max": 20,
    "vida": 100,
    "vida_max": 100,
    "dano": 25,
}

# Função para criar um NPC com atributos aleatórios
def criar_npc(level):
    novo_npc = {
        "nome": f"Monstro n°{level}",
        "level": level,
        "dano": 5 * level,
        "vida": 100 * level,
        "vida_max": 100 * level,
        "exp": 10 * level
    }
    if level == 0 and novo_npc["vida"] == 0 and novo_npc["exp"] == 0:
        novo_npc["vida"] = 50
        novo_npc["vida_max"] = 50
        novo_npc["level"] = 1
        novo_npc["dano"] = 5
        novo_npc["exp"] = 10
        return novo_npc
    else:
        return novo_npc

# Função para gerar NPCs e adicioná-los à lista de NPCs
def gerar_npcs(n_npcs):
 for a in range(n_npcs):                  
   npc = criar_npc(a) # Gera um nível de NPC aleatório 
   lista_npcs.append(npc) 

# Função para exibir os NPCs gerados
def exibir_npcs():
 print("\n===== NPCs Gerados =====")
 for npc in lista_npcs:
    print(
      f"Nome: {npc['nome']} | Level: {npc['level']} | Dano: {npc['dano']} | Vida: {npc['vida']}/{npc['vida_max']} | Exp: {npc['exp']}/{npc['exp']}"
    )

def exibir_npc(npc):
    print("\n===== NPC Selecionado =====")
    print(
        f"Nome: {npc['nome']} // Level: {npc['level']} // Dano: {npc['dano']} // HP: {npc['hp']} // EXP: {npc['exp']}"
    )

def exibir_player():
 print("\n===== Jogador =====")
 print(
      f"Nome: {player['nome']} | Level: {player['level']} | Dano: {player['dano']} | Vida: {player['vida']}/{player['vida_max']} | Exp: {player['exp']}/{player['exp_max']}"
    )  

# dano do jogador
def atacar_npc(npc): 
    dano_causado = randint(0, player["dano"] * player["level"]) # O dano causado pelo jogador é aleatório 
    npc["vida"] -= dano_causado
    return dano_causado

# dano do npc
def atacar_player(player, npc): 
    dano_causado = randint(0, npc["dano"] * npc["level"])  # mesma coisa, o dano do npc é aleatório
    player["vida"] -= dano_causado
    return dano_causado


def exibir_info_batalha(player, npc, dano_jogador, dano_npc): 
    print(f"\nVida do Jogador: {player['vida']}/{player['vida_max']} | "
          f"Vida do NPC: {npc['vida']}/{npc['vida_max']}")
    print(f"O jogador causou: {dano_jogador} de dano, e o NPC causou: {dano_npc} de dano.")
    print("================================================")

def reset_player():
   player["vida"] = player["vida_max"] # Reseta a vida do jogador para o máximo

def level_up_player():
    if player["exp"] == player["exp_max"]:
        player["level"] += 1 # Aumenta o nível do jogador
        player["exp_max"] *= 2 # Aumenta a experiência máxima necessária para o próximo nível
        player["exp"] = 0 # Reseta a experiência do jogador para 0, para não acumular experiência
        
    if player["level"] > 1:
        player["vida_max"] += 20
        player["dano"] += 5 # Aumenta a vida máxima e o dano do jogador a cada nível
        player["vida"] = player["vida_max"]
    
def iniciar_batalha(player, npc):
    while player["vida"] > 0 and npc["vida"] > 0: # enquanto o jogador e o NPC estiverem vivos, a batalha continua
        dano_jogador = atacar_npc(npc)
        dano_npc = atacar_player(player, npc)
        exibir_info_batalha(player, npc, dano_jogador, dano_npc)

    if player["vida"] > 0:
       print(f"\n{player["nome"]} venceu a batalha! E ganhou {npc["exp"]} de experiência") # Exibe mensagem de vitória
       player["exp"] += npc["exp"] # Adiciona a experiência do NPC à experiência do jogador

    else:
        print(f"\n{npc['nome']} venceu a batalha!")
        print(f"{player['nome']} perdeu a batalha e não ganhou experiência.") # exibe mensagem de derrota

    level_up_player() # Verifica se o jogador subiu de nível
    reset_player() # Reseta a vida do jogador para o máximo
    exibir_player() # Exibe as informações atualizadas do jogador

def iniciar_jogo():
    gerar_npcs(5)  # Gera 5 NPCs e preenche a lista

    exibir_npcs()  # (Opcional) Exibe todos os NPCs gerados

    index = 0
    continuar = True

    while continuar and index < len(lista_npcs):
        novo_npc = lista_npcs[index]
        print(f"\n===== Batalha de {player['nome']} com {novo_npc['nome']} =====")
        iniciar_batalha(player, novo_npc)

        if index + 1 < len(lista_npcs):
            resposta = input("Deseja lutar com o próximo monstro? (s/n): ")
            if resposta != "s":
                continuar = False
        index += 1

    print("\nFim do jogo!")

iniciar_jogo()
