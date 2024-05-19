from Configurações.Config import *



# variavel para controle do player do jogador
comandos = [[False], [False], [False], [False]] # (melhorar depois)

# lista para juntar os objetos das classes
grupo_projeteis = {}
grupo_processadores = {}
grupo_players = {}

clock = pygame.time.Clock()

# variaveis para contar o fps
contador_frames = 0
tempo_inicio = time.time()