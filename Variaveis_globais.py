from Config import *

# ajuda a selecionar o melhor individuo de cada geração
melhor_tempo = 0

melhor_individuo = []

contador_geracoes = 0

# listas das gerações anteriores
geracao_avo = []
geracao_anterior = []

# cria a estrutura da geração, para ser preenchida depois
geracao_atual = []
for individuo in range(numero_players):
    geracao_atual.append([])

# listas usadas na criação de uma nova geração
juncao_de_geracoes = []
valores_proporcionais = []
ja_sorteados = []

# variavel para ajudar a manter sempre o melhor player
primeiro_individuo = 0

# variavel para ajudar a direcionar os primeiros projeteis exatamente na direção do surgimento do player, para eliminar os piores
primeiro_inimigo = 0

# variavel para controle do player do jogador
comandos = [[False], [False], [False], [False]]

# lista para juntar os objetos das classes
grupo_inimigos = []
grupo_processadores = []
grupo_players = []

clock = pygame.time.Clock()

# variaveis para contar o fps
contador = 0
tempo_inicio = time.time()

partida_atual_da_geracao = 0