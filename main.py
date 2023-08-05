from Config import *
from Projeteis import *
from Criação_de_Rede import *
from Player import *


class Colisoes:
    def __init__(self):
        pass

    # função para conferir as colisões com o player
    def colisao_player_inimigo(self):
        global melhor_tempo, melhor_peso_primeira_camada_oculta, \
            melhor_peso_camada_de_saida, contador_geracoes, grupo_players, geracao_atual

        # para evitar que um individuo seja atingido por um inimigo e saia do limite da tela ao mesmo tempo (daria erro)
        self.colidiu = False

        # confere se cada inimigo colidiu com o player
        for player in grupo_players:
            for inimigo in grupo_inimigos:
                if player.rect_player.colliderect(inimigo.rect_inimigo):

                    # se sim, vai remover o player do grupo de players
                    grupo_players.remove(player)

                    # obter o tempo de vida do individuo
                    tempo_de_vida = player.funcao_de_perda()

                    # enviar os pesos do individuo para a lista da geração
                    pesos_individuo = []
                    pesos_individuo.append([tempo_de_vida])
                    pesos_individuo.append(player.grupo_neuronios_primeira_camada_oculta)
                    pesos_individuo.append(player.grupo_neuronios_camada_de_saida)

                    geracao_atual.append(pesos_individuo)

                    # se o tempo de vida dele for maior que o do melhor individuo, ele se torna o melhor
                    if tempo_de_vida > melhor_tempo:
                        melhor_tempo = tempo_de_vida
                        melhor_peso_primeira_camada_oculta = []
                        melhor_peso_camada_de_saida = []

                        # seus pesos são guardados em um lugar separado
                        for neuronio in player.grupo_neuronios_primeira_camada_oculta:
                            melhor_peso_primeira_camada_oculta.append(neuronio)

                        for neuronio in player.grupo_neuronios_camada_de_saida:
                            melhor_peso_camada_de_saida.append(neuronio)

                    # avisa que o player já colidiu
                    self.colidiu = True

                    # se um inimigo já tiver colidido, não é mais necessario fazer mais verificações
                    break

    def colisao_player_tela(self):
        global melhor_tempo, geracao_atual

        # confere se o player saiu dos limites da tela
        for player in grupo_players:
            if player.rect_player.bottom < 0 or player.rect_player.top > altura or \
                    player.rect_player.left < 0 or player.rect_player.right > largura and not self.colidiu:

                # se saiu, faz a mesma coisa da colisão com um inimigo
                if player in grupo_players:
                    grupo_players.remove(player)

                    tempo_de_vida = player.funcao_de_perda()

                    pesos_individuo = []
                    pesos_individuo.append([tempo_de_vida])
                    pesos_individuo.append(player.grupo_neuronios_primeira_camada_oculta)
                    pesos_individuo.append(player.grupo_neuronios_camada_de_saida)

                    geracao_atual.append(pesos_individuo)

                    # so vai para "pódio" de melhor individuo se for pelo menos 10% melhor que o atual melhor
                    if tempo_de_vida > melhor_tempo * 1.1:
                        melhor_tempo = tempo_de_vida
                        melhor_peso_primeira_camada_oculta = []
                        melhor_peso_camada_de_saida = []

                        for neuronio in player.grupo_neuronios_primeira_camada_oculta:
                            melhor_peso_primeira_camada_oculta.append(neuronio)

                        for neuronio in player.grupo_neuronios_camada_de_saida:
                            melhor_peso_camada_de_saida.append(neuronio)

    def update(self):
        self.colisao_player_inimigo()
        self.colisao_player_tela()


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


