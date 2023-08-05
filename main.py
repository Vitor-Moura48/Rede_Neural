from Config import *
from Projeteis import *
from Criação_de_Rede import *
from Player import *
from Colisões import *


# cria classe de colisões
colisoes = Colisoes()


# função para criar os objetos
def criar_objetos(quantidade_inimigos, quantidade_playes):

    for i in range(quantidade_inimigos):
        projetil = Inimigo()
        grupo_inimigos.append(projetil)
    for i in range(quantidade_playes):
        player = Player()
        grupo_players.append(player)


criar_objetos(20, 1500)

# variaveis para ajudar a contar fps
tempo_inicio = time.time()
contador = 0

# cria um limitador de fps
clock = pygame.time.Clock()

# loop principal
while True:

    # lógica para contar o fps
    contador += 1
    tempo_atual = time.time()

    if (tempo_atual - tempo_inicio) > 1:
        print(f'fps {contador}')

        contador = 0
        tempo_inicio = tempo_atual

    # atualiza todos os objetos
    for inimigo in grupo_inimigos:
        inimigo.update()
    for player in grupo_players:
        player.update()
    colisoes.update()

    

    # confere se eu cliquei para sair
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
            sys.exit()

    # se todos os players foram mortos
    if len(grupo_players) == 0:

        # registra que uma geração foi completa
        contador_geracoes += 1

        valores_proporcionais = []

        # zera a variavel que elimina os piores players
        primeiro_inimigo = 0

        # zera os inimigos e recria todos logo a frente
        grupo_inimigos = []

        # printa o melhor tempo
        print(f'melhor tempo {melhor_tempo}')

        # pega a geração atual e passa ela paga as gerações passadas, se for a primeira duplica ela
        if contador_geracoes == 1:
            geracao_avo = geracao_atual
            geracao_anterior = geracao_atual

        else:
            geracao_avo = geracao_anterior
            geracao_anterior = geracao_atual

        # junta as duas gerações mais recentes e organiza os individuos pela recompensa obtida por cada um
        juncao_de_geracoes = geracao_avo + geracao_anterior
        juncao_de_geracoes.sort(key=lambda x: x[0])

        total_de_recompesa = 0

        # soma todas as recompensas dos individuos
        for individuo in range(len(juncao_de_geracoes)):
            total_de_recompesa += int(juncao_de_geracoes[individuo][0][0])

        # adiciona proporcionalmente um valor de acordo com a recompensa de cada individuo (para a roleta)
        for individuo in range(len(juncao_de_geracoes)):
            if individuo == 0:
                valores_proporcionais.append(juncao_de_geracoes[individuo][0][0] / total_de_recompesa)


                # soma o valor anterior com o do individuo (para manter os valores "progredindo")
            else:
                valores_proporcionais.append(valores_proporcionais[-1] +
                                             juncao_de_geracoes[individuo][0][0] / total_de_recompesa)

        # zera a geração atual para ser preenchida novamente
        geracao_atual = []
        primeiro_individuo = True

        ja_sorteados = []

        criar_objetos(20, 1500)

    # define um limite de fps
    clock.tick(fps)

    # atualiza e preenche o display de preto
    pygame.display.update()
    tela.fill((000, 000, 000))


