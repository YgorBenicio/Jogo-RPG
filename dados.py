CLASSES = {
    "1": {"nome": "Guerreiro", "vida": 120, "dano": 16, "mana": 20},
    "2": {"nome": "Mago", "vida": 90, "dano": 13, "mana": 50},
    "3": {"nome": "Arqueiro", "vida": 100, "dano": 14, "mana": 30},
}

ULTIMA_FASE = 5
FASE_SECRETA = 6
PERDA_OURO_NA_MORTE = 25

PRECO_POCAO_VIDA = 30
PRECO_POCAO_MANA = 30

TIERS = {1: (7, 22), 2: (23, 40), 3: (41, 60)}

BAU_TIERS = {
    1: [70, 25, 5],
    2: [50, 35, 15],
    3: [30, 45, 25],
    4: [15, 45, 40],
    5: [5, 35, 60],
    6: [0, 10, 90],
}

ARMAS = {
    "Espada": "dano do ataque normal + nível / 2",
    "Escudo": "dano recebido - nível / 3",
    "Cajado": "dano do ataque especial + nível",
    "Arco": "chance de crítico + nível / 2 (%)",
}

EXTRAS = {
    "Espada": "roubo de vida: recupera 10% do dano causado por tier",
    "Escudo": "reflexo: devolve 10% do dano recebido por tier",
    "Cajado": "atordoamento: 10% de chance por tier no especial",
    "Arco": "flecha dupla: 10% de chance por tier no ataque normal",
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
            "nome": "Lobo", "vida": 98, "dano": 13, "exp": 14, "ouro": 25,
            "especial": {"nome": "Mordida Cortante", "chance": 25, "multiplicador": 2,
                         "efeitos": ["sangramento"], "chance_efeito": 60},
        },
        "boss": {
            "nome": "Lobo Alfa", "vida": 234, "dano": 18, "exp": 30, "ouro": 70,
            "especial": {"nome": "Garras Dilacerantes", "chance": 35, "multiplicador": 2.5,
                         "efeitos": ["sangramento", "veneno"], "chance_efeito": 70},
        },
    },
    2: {
        "nome": "Deserto Escaldante",
        "sufixo": "do Deserto",
        "evento": {"nome": "Uma tempestade de areia sopra", "chance": 25, "dano": 10},
        "mob": {
            "nome": "Escorpião Gigante", "vida": 144, "dano": 18, "exp": 20, "ouro": 30,
            "especial": {"nome": "Ferrão Venenoso", "chance": 25, "multiplicador": 2,
                         "efeitos": ["veneno"], "chance_efeito": 60},
        },
        "boss": {
            "nome": "Esfinge de Areia", "vida": 342, "dano": 22, "exp": 45, "ouro": 90,
            "especial": {"nome": "Maldição das Dunas", "chance": 35, "multiplicador": 2.5,
                         "efeitos": ["veneno", "maldicao"], "chance_efeito": 70},
        },
    },
    3: {
        "nome": "Vulcão Ardente",
        "sufixo": "do Vulcão",
        "evento": {"nome": "Lava cai do teto", "chance": 25, "dano": 16},
        "mob": {
            "nome": "Golem de Lava", "vida": 198, "dano": 22, "exp": 28, "ouro": 35,
            "especial": {"nome": "Soco Ardente", "chance": 25, "multiplicador": 2,
                         "efeitos": ["queimadura"], "chance_efeito": 60},
        },
        "boss": {
            "nome": "Dragão de Magma", "vida": 468, "dano": 28, "exp": 60, "ouro": 100,
            "especial": {"nome": "Sopro de Magma", "chance": 35, "multiplicador": 2.5,
                         "efeitos": ["queimadura", "sangramento"], "chance_efeito": 70},
        },
    },
    4: {
        "nome": "Cripta Esquecida",
        "sufixo": "da Cripta",
        "evento": {"nome": "Ossos desabam do teto", "chance": 20, "dano": 14},
        "mob": {
            "nome": "Esqueleto Guerreiro", "vida": 252, "dano": 27, "exp": 36, "ouro": 40,
            "especial": {"nome": "Golpe Sombrio", "chance": 25, "multiplicador": 2,
                         "efeitos": ["maldicao"], "chance_efeito": 60},
        },
        "boss": {
            "nome": "Lorde Necromante", "vida": 576, "dano": 33, "exp": 80, "ouro": 110,
            "especial": {"nome": "Toque da Morte", "chance": 35, "multiplicador": 2.5,
                         "efeitos": ["maldicao", "veneno"], "chance_efeito": 70},
        },
    },
    5: {
        "nome": "Montanha Gelada",
        "sufixo": "da Montanha",
        "evento": {"nome": "Uma avalanche desce a encosta", "chance": 20, "dano": 20},
        "mob": {
            "nome": "Yeti", "vida": 324, "dano": 33, "exp": 45, "ouro": 45,
            "especial": {"nome": "Rugido Congelante", "chance": 25, "multiplicador": 2,
                         "efeitos": ["frio"], "chance_efeito": 60},
        },
        "boss": {
            "nome": "Dragão de Gelo", "vida": 756, "dano": 39, "exp": 110, "ouro": 130,
            "especial": {"nome": "Sopro Glacial", "chance": 35, "multiplicador": 2.5,
                         "efeitos": ["frio", "sangramento"], "chance_efeito": 70},
        },
    },
    6: {
        "nome": "Abismo Esquecido",
        "sufixo": "do Abismo",
        "evento": {"nome": "Fissuras se abrem no chão", "chance": 25, "dano": 24},
        "boss": {
            "nome": "Guardião do Abismo", "vida": 1080, "dano": 48, "exp": 200, "ouro": 400,
            "especial": {"nome": "Olhar do Vazio", "chance": 35, "multiplicador": 2.5,
                         "efeitos": ["maldicao", "queimadura", "frio"], "chance_efeito": 70},
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
    6: [
        {"nome": "Cajado do Vazio", "tipo": "Cajado", "tier": 3, "nivel": 60, "preco": 2400},
        {"nome": "Arco do Abismo", "tipo": "Arco", "tier": 3, "nivel": 60, "preco": 2300},
    ],
}
