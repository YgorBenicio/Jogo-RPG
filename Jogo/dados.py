CLASSES = {
    "1": {"nome": "Guerreiro", "vida": 120, "dano": 16, "mana": 20},
    "2": {"nome": "Mago", "vida": 90, "dano": 13, "mana": 50},
    "3": {"nome": "Arqueiro", "vida": 100, "dano": 14, "mana": 30},
}

PRECO_POCAO_VIDA = 30
PRECO_POCAO_MANA = 30

TIERS = {1: (7, 22), 2: (23, 40), 3: (41, 60)}

BAU_TIERS = {
    1: [70, 25, 5],
    2: [50, 35, 15],
    3: [30, 45, 25],
    4: [15, 45, 40],
    5: [5, 35, 60],
}

ARMAS = {
    "Espada": "dano do ataque normal + nível / 2",
    "Escudo": "dano recebido - nível / 3",
    "Cajado": "dano do ataque especial + nível",
    "Arco": "chance de crítico + nível / 2 (%)",
}

EFEITOS = {
    "sangramento": {"nome": "Sangramento", "dano": 4, "turnos": 3},
    "veneno": {"nome": "Veneno", "dano": 5, "turnos": 3},
    "queimadura": {"nome": "Queimadura", "dano": 7, "turnos": 3},
    "maldicao": {"nome": "Maldição", "dano": 8, "turnos": 3},
    "frio": {"nome": "Hipotermia", "dano": 9, "turnos": 3},
}

FASES = {
    1: {
        "nome": "Floresta Sombria",
        "sufixo": "da Floresta",
        "evento": {"nome": "Um galho pesado despenca", "chance": 20, "dano": 10},
        "mob": {
            "nome": "Lobo", "vida": 82, "dano": 11, "exp": 14, "ouro": 25,
            "especial": {"nome": "Mordida Cortante", "chance": 25, "multiplicador": 1.5,
                         "efeito": "sangramento", "chance_efeito": 50},
        },
        "boss": {
            "nome": "Lobo Alfa", "vida": 195, "dano": 15, "exp": 30, "ouro": 70,
            "especial": {"nome": "Garras Dilacerantes", "chance": 30, "multiplicador": 2,
                         "efeito": "sangramento", "chance_efeito": 60},
        },
    },
    2: {
        "nome": "Deserto Escaldante",
        "sufixo": "do Deserto",
        "evento": {"nome": "Uma tempestade de areia sopra", "chance": 25, "dano": 10},
        "mob": {
            "nome": "Escorpião Gigante", "vida": 120, "dano": 15, "exp": 20, "ouro": 30,
            "especial": {"nome": "Ferrão Venenoso", "chance": 25, "multiplicador": 1.5,
                         "efeito": "veneno", "chance_efeito": 50},
        },
        "boss": {
            "nome": "Esfinge de Areia", "vida": 285, "dano": 19, "exp": 45, "ouro": 90,
            "especial": {"nome": "Maldição das Dunas", "chance": 30, "multiplicador": 2,
                         "efeito": "veneno", "chance_efeito": 60},
        },
    },
    3: {
        "nome": "Vulcão Ardente",
        "sufixo": "do Vulcão",
        "evento": {"nome": "Lava cai do teto", "chance": 25, "dano": 16},
        "mob": {
            "nome": "Golem de Lava", "vida": 165, "dano": 19, "exp": 28, "ouro": 35,
            "especial": {"nome": "Soco Ardente", "chance": 25, "multiplicador": 1.5,
                         "efeito": "queimadura", "chance_efeito": 50},
        },
        "boss": {
            "nome": "Dragão de Magma", "vida": 390, "dano": 24, "exp": 60, "ouro": 100,
            "especial": {"nome": "Sopro de Magma", "chance": 30, "multiplicador": 2,
                         "efeito": "queimadura", "chance_efeito": 60},
        },
    },
    4: {
        "nome": "Cripta Esquecida",
        "sufixo": "da Cripta",
        "evento": {"nome": "Ossos desabam do teto", "chance": 20, "dano": 14},
        "mob": {
            "nome": "Esqueleto Guerreiro", "vida": 210, "dano": 23, "exp": 36, "ouro": 40,
            "especial": {"nome": "Golpe Sombrio", "chance": 25, "multiplicador": 1.5,
                         "efeito": "maldicao", "chance_efeito": 50},
        },
        "boss": {
            "nome": "Lorde Necromante", "vida": 480, "dano": 28, "exp": 80, "ouro": 110,
            "especial": {"nome": "Toque da Morte", "chance": 30, "multiplicador": 2,
                         "efeito": "maldicao", "chance_efeito": 60},
        },
    },
    5: {
        "nome": "Montanha Gelada",
        "sufixo": "da Montanha",
        "evento": {"nome": "Uma avalanche desce a encosta", "chance": 20, "dano": 20},
        "mob": {
            "nome": "Yeti", "vida": 270, "dano": 28, "exp": 45, "ouro": 45,
            "especial": {"nome": "Rugido Congelante", "chance": 25, "multiplicador": 1.5,
                         "efeito": "frio", "chance_efeito": 50},
        },
        "boss": {
            "nome": "Dragão de Gelo", "vida": 630, "dano": 33, "exp": 110, "ouro": 130,
            "especial": {"nome": "Sopro Glacial", "chance": 30, "multiplicador": 2,
                         "efeito": "frio", "chance_efeito": 60},
        },
    },
}

LOJA = {
    1: [
        {"nome": "Lâmina do Caçador", "tipo": "Espada", "tier": 2, "nivel": 30, "preco": 400},
        {"nome": "Escudo de Carvalho", "tipo": "Escudo", "tier": 2, "nivel": 28, "preco": 380},
    ],
    2: [
        {"nome": "Arco das Dunas", "tipo": "Arco", "tier": 2, "nivel": 38, "preco": 600},
        {"nome": "Cajado do Oásis", "tipo": "Cajado", "tier": 2, "nivel": 36, "preco": 580},
    ],
    3: [
        {"nome": "Lâmina de Obsidiana", "tipo": "Espada", "tier": 3, "nivel": 48, "preco": 900},
        {"nome": "Escudo de Magma", "tipo": "Escudo", "tier": 3, "nivel": 45, "preco": 880},
    ],
    4: [
        {"nome": "Cajado Necrótico", "tipo": "Cajado", "tier": 3, "nivel": 52, "preco": 1200},
        {"nome": "Arco de Ossos", "tipo": "Arco", "tier": 3, "nivel": 50, "preco": 1150},
    ],
    5: [
        {"nome": "Lâmina Glacial", "tipo": "Espada", "tier": 3, "nivel": 58, "preco": 1600},
        {"nome": "Égide do Gelo", "tipo": "Escudo", "tier": 3, "nivel": 57, "preco": 1550},
    ],
}
