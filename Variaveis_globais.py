from Config import pygame, time

# ajuda a selecionar o melhor individuo de cada geração
melhor_tempo = 0

melhor_peso_primeira_camada_oculta = []
melhor_peso_camada_de_saida = []

contador_geracoes = 0

geracao_avo = []
geracao_anterior = []
geracao_atual = []

juncao_de_geracoes = []
valores_proporcionais = []

ja_sorteados = []

# variavel para ajudar a manter sempre o melhor player
primeiro_individuo = True

# variavel para ajudar a direcionar os primeiros projeteis exatamente na direção do surgimento do player, para eliminar os piores
primeiro_inimigo = 0

# lista para juntar os objetos das classes
grupo_inimigos = []
grupo_players = []

clock = pygame.time.Clock()

contador = 0
tempo_inicio = time.time()