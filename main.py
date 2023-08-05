from Config import *
import Variaveis_globais
from Projeteis import *
from Criação_de_Rede import *
from Player import *
from Colisões import *


# função para criar os objetos
def criar_objetos(quantidade_inimigos, quantidade_playes):

    for i in range(quantidade_inimigos):
        projetil = Inimigo()
        Variaveis_globais.grupo_inimigos.append(projetil)
    for i in range(quantidade_playes):
        player = Player()
        Variaveis_globais.grupo_players.append(player)


 # lógica para contar o fps
def exibir_fps():
    global mensagem_fps_para_tela

    Variaveis_globais.contador += 1
    tempo_atual = time.time()

    if (tempo_atual - Variaveis_globais.tempo_inicio) > 1:

        mensagem_fps = "fps " + str(Variaveis_globais.contador)
        mensagem_fps_para_tela = fonte.render(mensagem_fps, True, (255, 000, 000))

        print(f'fps {Variaveis_globais.contador}')

        Variaveis_globais.contador = 0
        Variaveis_globais.tempo_inicio = tempo_atual
    
     # exibe a taxa de fps no display
    tela.blit(mensagem_fps_para_tela, (1350, 50))


# atualiza todos os objetos
def atualizar_objetos():

    for inimigo in Variaveis_globais.grupo_inimigos:
        inimigo.update()
    for player in Variaveis_globais.grupo_players:
        player.update()
    colisoes.update()

def nova_geracao():

        # registra que uma geração foi completa
        Variaveis_globais.contador_geracoes += 1

        Variaveis_globais.valores_proporcionais = []

        # zera a variavel que elimina os piores players
        Variaveis_globais.primeiro_inimigo = 0

        # zera os inimigos e recria todos logo a frente
        Variaveis_globais.grupo_inimigos = []

        # printa o melhor tempo
        print(f'melhor tempo {Variaveis_globais.melhor_tempo}')

        # pega a geração atual e passa ela paga as gerações passadas, se for a primeira duplica ela
        if Variaveis_globais.contador_geracoes == 1:
            Variaveis_globais.geracao_avo = Variaveis_globais.geracao_atual
            Variaveis_globais.geracao_anterior = Variaveis_globais.geracao_atual

        else:
            Variaveis_globais.geracao_avo = Variaveis_globais.geracao_anterior
            Variaveis_globais.geracao_anterior = Variaveis_globais.geracao_atual

        # junta as duas gerações mais recentes e organiza os individuos pela recompensa obtida por cada um
        Variaveis_globais.juncao_de_geracoes = Variaveis_globais.geracao_avo + Variaveis_globais.geracao_anterior
        Variaveis_globais.juncao_de_geracoes.sort(key=lambda x: x[0])

        total_de_recompesa = 0

        # soma todas as recompensas dos individuos
        for individuo in range(len(Variaveis_globais.juncao_de_geracoes)):
            total_de_recompesa += int(Variaveis_globais.juncao_de_geracoes[individuo][0][0])

        # adiciona proporcionalmente um valor de acordo com a recompensa de cada individuo (para a roleta)
        for individuo in range(len(Variaveis_globais.juncao_de_geracoes)):
            if individuo == 0:
                Variaveis_globais.valores_proporcionais.append(Variaveis_globais.juncao_de_geracoes[individuo][0][0] / total_de_recompesa)


                # soma o valor anterior com o do individuo (para manter os valores "progredindo")
            else:
                Variaveis_globais.valores_proporcionais.append(Variaveis_globais.valores_proporcionais[-1] +
                                             Variaveis_globais.juncao_de_geracoes[individuo][0][0] / total_de_recompesa)

        # zera a geração atual para ser preenchida novamente
        Variaveis_globais.geracao_atual = []
        Variaveis_globais.primeiro_individuo = True

        Variaveis_globais.ja_sorteados = []

        criar_objetos(20, 1500)


criar_objetos(20, 1500)

# cria classe de colisões
colisoes = Colisoes()


# loop principal
while True:

    # função para exibir o fps
    exibir_fps()

    # função para dar update em todos os objetos
    atualizar_objetos()

    # confere o clique para sair
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
            sys.exit()

    # se todos os players foram "mortos", cria uma nova geração
    if len(Variaveis_globais.grupo_players) == 0:
        nova_geracao()

    # define um limite de fps
    Variaveis_globais.clock.tick(fps)

    # atualiza e preenche o display de preto
    pygame.display.update()
    tela.fill((000, 000, 000))


