from Configurações.Config import *
import Configurações.Global as Global
from Jogo.Projeteis import *
from Jogo.Player import *
from Jogo.Colisões import *
from Rede_Neural import estrategia_evolutiva

# função para criar os objetos
def criar_objetos(quantidade_projeteis, quantidade_playes):   

    estrategia_evolutiva.gerenciador.nova_partida()

    # define a posiçãao e direção inicial (opcional)
    coordendas_iniciais = [[largura + 20, altura / 2, numpy.radians(180)], [largura / 2, -20, numpy.radians(90)], [-20, altura / 2, 0], [largura / 2, altura + 20, numpy.radians(270)]]
    # cria os projeteis a partir do valor definido em Config
    for i in range(quantidade_projeteis):
        if i > 0:
            projetil = Projeteis()       
        else:
            projetil = Projeteis(choice(coordendas_iniciais)) # escolhe um projétil para mirar no centro de pawn (para eliminar os que ficam parados)
        Global.grupo_projeteis[i] = projetil 

# atualiza todos os objetos
def atualizar_objetos():

    # função para exibir o fps
    #visualizador.dados.update()

    for projetil in Global.grupo_projeteis.values():
        projetil.update()

    for agente in estrategia_evolutiva.gerenciador.agentes:
        agente.update()

    # confere as colisões
    colisoes.update()

# função para criar uma nova geração
def nova_geracao():
    
    # zera algumas variaveis que serão usadas depois
    Global.individuos_elite = 0
    Global.juncao_de_geracoes = []     
    Global.grupo_projeteis = {}

     # salva algumas informações
    with open("Rede_neural/informacoes.json", 'w') as arquivo:
        json.dump([Global.contador_geracoes], arquivo)

    melhor_tempo_da_geracao = 0
    # divide a recompensa pela quantidade de partidas para fazer a media de recompensa 
    for individuo in range(numero_players):
        Global.geracao_atual[individuo][0][0] /= partidas_por_geracao

        # marca o melhor tempo da geração
        if Global.geracao_atual[individuo][0][0] > melhor_tempo_da_geracao:
            melhor_tempo_da_geracao = Global.geracao_atual[individuo][0][0]      

            # confere se existe um novo melhor individuo
            if Global.geracao_atual[individuo][0][0] > Global.melhor_tempo:
                Global.melhor_tempo = Global.geracao_atual[individuo][0][0]
                Global.melhor_individuo = Global.geracao_atual[individuo]

                # tranforma os dados ndrray em listas normais 
                pesos_normalizados = [
                                        [neuronio.tolist() if isinstance(neuronio, numpy.ndarray) else neuronio for neuronio in camada]
                                        for camada in Global.melhor_individuo
                                        ]

                # se sim, adiciona ele em um arquivo csv
                with open("Rede_neural/melhor_individuo.json", 'w') as arquivo:
                    json.dump(pesos_normalizados, arquivo)

    # printa o melhor tempo geral e o melhor tempo dessa geração
    print(f'melhor tempo global: {Global.melhor_tempo}')
    print(f"melhor tempo da geração; {melhor_tempo_da_geracao}")

    # pega a geração atual e passa ela para as gerações passadas
    Global.geracao_avo = Global.geracao_anterior
    Global.geracao_anterior = Global.geracao_atual

    # salva a geração em um arquivo
    def salvar_geracao(geracao, nome_do_arquivo):
        
        with open(nome_do_arquivo, 'w') as arquivo:
            # tranforma os dados ndrray em listas normais 
            lista_geracao = [   
                                [
                                [neuronio.tolist() if isinstance(neuronio, numpy.ndarray) else neuronio for neuronio in camada]
                                for camada in individuo 
                                ]
                                for individuo in geracao
                            ]
            json.dump(lista_geracao, arquivo)
    
    salvar_geracao(Global.geracao_anterior, "Rede_Neural/geracao_anterior.json")
    salvar_geracao(Global.geracao_avo, "Rede_Neural/geracao_avo.json")

    # junta as duas gerações mais recentes e organiza os individuos pela recompensa obtida por cada um  
    Global.juncao_de_geracoes = Global.geracao_avo + Global.geracao_anterior
    Global.juncao_de_geracoes.sort(key=lambda x: x[0])

    # soma todas as recompensas dos individuos
    total_de_recompesa = sum(individuo[0][0] for individuo in Global.juncao_de_geracoes)

    # adiciona a proporção de recompensa do primeiro individuo
    Global.valores_proporcionais = [Global.juncao_de_geracoes[0][0][0] / total_de_recompesa]
    # adiciona proporcionalmente um valor de acordo com a recompensa de cada individuo (para a roleta)
    for individuo in range(1, len(Global.juncao_de_geracoes)):
        
        # soma o valor anterior com o do individuo (para manter os valores "progredindo")
        Global.valores_proporcionais.append(Global.valores_proporcionais[-1] + Global.juncao_de_geracoes[individuo][0][0] / total_de_recompesa)

    # zera a geração atual para ser preenchida novamente
    Global.geracao_atual = []

    # recria a estrutura da geração atual (vazia)
    for individuo in range(numero_players):
        Global.geracao_atual.append([])

    # cria ou recria os objetos
    criar_objetos(numero_projeteis, numero_players)

def nova_geracao_ou_nova_partida():

    # registra a conclusão de uma partida
    Global.partida_atual_da_geracao += 1    

    # zera a variavel que ajuda a eliminar os piores players
    Global.primeiro_inimigo = 0

    # confere se a quantidade escolhida de partidas por geração foi completa, se sim, cria a nova geração normalmente
    if Global.partida_atual_da_geracao >= partidas_por_geracao:

        # registra que uma geração foi completa
        Global.contador_geracoes += 1
        Global.partida_atual_da_geracao = 0

        # chama a função de criar uma nova geração
        nova_geracao()

    else:

        # zera os inimigos e recria todos depois
        Global.grupo_projeteis = {}

        criar_objetos(numero_projeteis, numero_players)

# função para verificar se o jogador movimentou o player e responder (melhorar depois)
def movimentacao_jogador():
   
   # define se o player está ativo ou não (o estado começa com: não ativo)
    estado_player1 = False
    estado_player2 = False

    # se a configuração for de um jogador, confere se ele está ativo
    if quantidade_jogadores == 1:
        if Global.grupo_players[-1].real and Global.grupo_players[-1].indice == 0:
            estado_player1 = True
            player1 = -1

    # se a configuração for de dois jogadores, confere se eles estão vivos e define os indices de cada um (de acordo com a situação)
    elif quantidade_jogadores == 2:

        if len(Global.grupo_players) > 1:

            # se o player 1 tiver indice -2, automaticamente os dois players estão vivos
            if Global.grupo_players[-2].indice == 0 and Global.grupo_players[-2].real:
                estado_player1 = True
                estado_player2 = True

                player1 = -2
                player2 = -1

            # se um dos dois players foram eliminados, confere se um dos dois ainda está vivo
            elif Global.grupo_players[-1].indice == 0 and Global.grupo_players[-1].real:
                estado_player1 = True
                player1 = -1
            elif Global.grupo_players[-1].indice == 1 and Global.grupo_players[-1].real:
                estado_player2 = True
                player2 = -1

        # se só houver um player possível, confere se esse player é o 1 ou o 2
        else:

            if Global.grupo_players[-1].indice == 0 and Global.grupo_players[-1].real:
                estado_player1 = True
                player1 = -1

            elif Global.grupo_players[-1].indice == 1 and Global.grupo_players[-1].real:
                estado_player2 = True
                player2 = -1

    # para movimentar o jogador 1
    if estado_player1:


        if pygame.key.get_pressed()[K_a]:
            Global.grupo_players[player1].posicao_x -= velocidade_ia

        if pygame.key.get_pressed()[K_d]:
            Global.grupo_players[player1].posicao_x += velocidade_ia

        if pygame.key.get_pressed()[K_w]:
            Global.grupo_players[player1].posicao_y -= velocidade_ia

        if pygame.key.get_pressed()[K_s]:
            Global.grupo_players[player1].posicao_y += velocidade_ia

    # para movimentar o jogador 2
    if estado_player2:

        if pygame.key.get_pressed()[K_LEFT]:
            Global.grupo_players[player2].posicao_x -= velocidade_ia

        if pygame.key.get_pressed()[K_RIGHT]:
            Global.grupo_players[player2].posicao_x += velocidade_ia

        if pygame.key.get_pressed()[K_UP]:
            Global.grupo_players[player2].posicao_y -= velocidade_ia

        if pygame.key.get_pressed()[K_DOWN]:
            Global.grupo_players[player2].posicao_y += velocidade_ia

def iniciar_save():

    # junta as duas gerações mais recentes e organiza os individuos pela recompensa obtida por cada um  
    Global.juncao_de_geracoes = Global.geracao_avo + Global.geracao_anterior
    Global.juncao_de_geracoes.sort(key=lambda x: x[0])

    # soma todas as recompensas dos individuos
    total_de_recompesa = sum(individuo[0][0] for individuo in Global.juncao_de_geracoes)
   
    Global.valores_proporcionais = [Global.juncao_de_geracoes[0][0][0] / total_de_recompesa]
    # adiciona proporcionalmente um valor de acordo com a recompensa de cada individuo (para a roleta)
    for individuo in range(1, len(Global.juncao_de_geracoes) - 1):

        # soma o valor anterior com o do individuo (para manter os valores "progredindo")
        Global.valores_proporcionais.append(Global.valores_proporcionais[-1] + Global.juncao_de_geracoes[individuo][0][0] / total_de_recompesa)
                    
    # zera a geração atual para ser preenchida novamente
    Global.geracao_atual = []
    # recria a estrutura da geração atual (vazia)
    for individuo in range(numero_players):
        Global.geracao_atual.append([])


estrategia_evolutiva.gerenciador = estrategia_evolutiva.GerenciadorNeural(500, 10, 0.4, Player)
criar_objetos(numero_projeteis, numero_players) # cria os objetos iniciais

# cria classe de colisões
colisoes = Colisoes()

