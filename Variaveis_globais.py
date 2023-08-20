from Config import *

# ajuda a selecionar o melhor individuo de cada geração
melhor_tempo = 0

melhor_individuo = []

contador_geracoes = 0

geracao_avo = []
geracao_anterior = []

geracao_atual = []
for individuo in range(numero_players):
    geracao_atual.append([])

juncao_de_geracoes = []
valores_proporcionais = []

ja_sorteados = []

# variavel para ajudar a manter sempre o melhor player
primeiro_individuo = 0

# variavel para ajudar a direcionar os primeiros projeteis exatamente na direção do surgimento do player, para eliminar os piores
primeiro_inimigo = 0

comandos = [[False], [False], [False], [False]]

# lista para juntar os objetos das classes
grupo_inimigos = []
grupo_processadores = []
grupo_players = []

clock = pygame.time.Clock()

contador = 0
tempo_inicio = time.time()

partida_atual_da_geracao = 0