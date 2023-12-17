from Configurações.Config import *
import Configurações.Variaveis_globais as Variaveis_globais
from Jogo.Projeteis import *
from Rede_Neural.Criação_de_Rede import *
from Rede_Neural.Processador import *
from Rede_Neural.Player import *
from Jogo.Colisões import *

# função para criar os objetos
def criar_objetos(quantidade_inimigos, quantidade_playes):   

    # cria os projeteis a partir do valor definido em Config
    for i in range(quantidade_inimigos):

        projetil = Projeteis()
        Variaveis_globais.grupo_projeteis[i] = projetil 

    # cria os players a partir do valor definido em Config
    for indice_do_player_na_geracao in range(quantidade_playes):

        # cria o player, que vai aparecer na tela
        player = Player(False, indice_do_player_na_geracao)

        # se for o início de uma nova geração ele cria a nova geração normalmente
        if Variaveis_globais.partida_atual_da_geracao == 0:

            # cria a rede para processar as entradas
            nova_rede = CriarRedeNeural()
            resultado = nova_rede.randomizar_resultados()
            processador = Processador(indice_do_player_na_geracao, resultado) 
         
        # se não, copia as redes daquela geração
        else:
            processador = Processador(indice_do_player_na_geracao, Variaveis_globais.geracao_atual[indice_do_player_na_geracao][1:])

        # adiciona do grupo de redes e players novamente
        Variaveis_globais.grupo_processadores[indice_do_player_na_geracao] = processador
        Variaveis_globais.grupo_players[indice_do_player_na_geracao] = player
    
    # condição para adicionar um player para o jogador
    if quantidade_jogadores > 0:

        # cria um ou dois players
        for i in range(quantidade_jogadores):
    
            player = Player(True, i)  # o index nesse caso registra quem é o primeiro e o segundo player
            Variaveis_globais.grupo_players[i] = player

# lógica para contar o fps
def exibir_fps():
    global mensagem_fps_para_tela

    Variaveis_globais.contador += 1
    tempo_atual = time.time()

    # a cada segundo, printa a quantidade de loops feitos
    if (tempo_atual - Variaveis_globais.tempo_inicio) > 1:

        mensagem_fps = "fps " + str(Variaveis_globais.contador)
        mensagem_fps_para_tela = fonte.render(mensagem_fps, True, (255, 000, 000))

        Variaveis_globais.contador = 0
        Variaveis_globais.tempo_inicio = tempo_atual
    
    # exibe a taxa de fps no display
    tela.blit(mensagem_fps_para_tela, (1350, 50))

# atualiza todos os objetos
def atualizar_objetos():
    for projetil in Variaveis_globais.grupo_projeteis.values():
        projetil.update()
    
    for processador in Variaveis_globais.grupo_processadores.values():
        processador.update()
    
    for player in Variaveis_globais.grupo_players.values():
        player.update()

    # confere as colisões
    colisoes.update()

# função para criar uma nova geração
def nova_geracao():
    
    # zera algumas variaveis que serão usadas depois
    Variaveis_globais.individuos_elite = 0
    Variaveis_globais.ja_sorteados = []
    Variaveis_globais.juncao_de_geracoes = []     
    Variaveis_globais.grupo_projeteis = {}

    melhor_tempo_da_geracao = 0
    # divide a recompensa pela quantidade de partidas para fazer a media de recompensa 
    for individuo in range(numero_players):
        Variaveis_globais.geracao_atual[individuo][0][0] /= partidas_por_geracao

        # marca o melhor tempo da geração
        if Variaveis_globais.geracao_atual[individuo][0][0] > melhor_tempo_da_geracao:
            melhor_tempo_da_geracao = Variaveis_globais.geracao_atual[individuo][0][0]      

            # confere se existe um novo melhor individuo
            if Variaveis_globais.geracao_atual[individuo][0][0] > Variaveis_globais.melhor_tempo:
                Variaveis_globais.melhor_tempo = Variaveis_globais.geracao_atual[individuo][0][0]
                Variaveis_globais.melhor_individuo = Variaveis_globais.geracao_atual[individuo]

                # tranforma os dados ndrray em listas normais 
                pesos_normalizados = [neuronio.tolist() if isinstance(neuronio, numpy.ndarray) else neuronio 
                                        for camada in Variaveis_globais.melhor_individuo
                                            for neuronio in camada]
                
                # se sim, adiciona ele em um arquivo csv
                with open("Rede_neural/melhor_individuo.json", 'w') as arquivo:
                    json.dump(pesos_normalizados, arquivo)

    # printa o melhor tempo
    print(f'melhor tempo global: {Variaveis_globais.melhor_tempo}')
    print(f"melhor tempo da partida; {melhor_tempo_da_geracao}")

    # pega a geração atual e passa ela para as gerações passadas
    Variaveis_globais.geracao_avo = Variaveis_globais.geracao_anterior
    Variaveis_globais.geracao_anterior = Variaveis_globais.geracao_atual

    # junta as duas gerações mais recentes e organiza os individuos pela recompensa obtida por cada um  
    Variaveis_globais.juncao_de_geracoes = Variaveis_globais.geracao_avo + Variaveis_globais.geracao_anterior
    Variaveis_globais.juncao_de_geracoes.sort(key=lambda x: x[0])

    # soma todas as recompensas dos individuos
    total_de_recompesa = sum(individuo[0][0] for individuo in Variaveis_globais.juncao_de_geracoes)
   
    Variaveis_globais.valores_proporcionais = [Variaveis_globais.juncao_de_geracoes[individuo][0][0] / total_de_recompesa]
    # adiciona proporcionalmente um valor de acordo com a recompensa de cada individuo (para a roleta)
    for individuo in range(1, len(Variaveis_globais.juncao_de_geracoes) - 1):

        # soma o valor anterior com o do individuo (para manter os valores "progredindo")
        Variaveis_globais.valores_proporcionais.append(Variaveis_globais.valores_proporcionais[-1] + Variaveis_globais.juncao_de_geracoes[individuo][0][0] / total_de_recompesa)
                    
    # zera a geração atual para ser preenchida novamente
    Variaveis_globais.geracao_atual = []
    # recria a estrutura da geração atual (vazia)
    for individuo in range(numero_players):
        Variaveis_globais.geracao_atual.append([])

    # cria ou recria os objetos
    criar_objetos(numero_projeteis, numero_players)

def nova_geracao_ou_nova_partida():

    # registra a conclusão de uma partida
    Variaveis_globais.partida_atual_da_geracao += 1    

    # zera a variavel que ajuda a eliminar os piores players
    Variaveis_globais.primeiro_inimigo = 0

    # confere se a quantidade escolhida de partidas por geração foi completa, se sim, cria a nova geração normalmente
    if Variaveis_globais.partida_atual_da_geracao == partidas_por_geracao:

        # registra que uma geração foi completa
        Variaveis_globais.contador_geracoes += 1
        Variaveis_globais.partida_atual_da_geracao = 0

        # chama a função de criar uma nova geração
        nova_geracao()

    else:
        
        # zera os inimigos e recria todos depois
        Variaveis_globais.grupo_projeteis = {}

        criar_objetos(numero_projeteis, numero_players)

# função para verificar se o jogador movimentou o player e responder (melhorar depois)
def movimentacao_jogador():
   
   # define se o player está ativo ou não (o estado começa com: não ativo)
    estado_player1 = False
    estado_player2 = False

    # se a configuração for de um jogador, confere se ele está ativo
    if quantidade_jogadores == 1:
        if Variaveis_globais.grupo_players[-1].real and Variaveis_globais.grupo_players[-1].indice == 0:
            estado_player1 = True
            player1 = -1

    # se a configuração for de dois jogadores, confere se eles estão vivos e define os indices de cada um (de acordo com a situação)
    elif quantidade_jogadores == 2:

        if len(Variaveis_globais.grupo_players) > 1:

            # se o player 1 tiver indice -2, automaticamente os dois players estão vivos
            if Variaveis_globais.grupo_players[-2].indice == 0 and Variaveis_globais.grupo_players[-2].real:
                estado_player1 = True
                estado_player2 = True

                player1 = -2
                player2 = -1

            # se um dos dois players foram eliminados, confere se um dos dois ainda está vivo
            elif Variaveis_globais.grupo_players[-1].indice == 0 and Variaveis_globais.grupo_players[-1].real:
                estado_player1 = True
                player1 = -1
            elif Variaveis_globais.grupo_players[-1].indice == 1 and Variaveis_globais.grupo_players[-1].real:
                estado_player2 = True
                player2 = -1

        # se só houver um player possível, confere se esse player é o 1 ou o 2
        else:
            if Variaveis_globais.grupo_players[-1].indice == 0 and Variaveis_globais.grupo_players[-1].real:
                estado_player1 = True
                player1 = -1

            elif Variaveis_globais.grupo_players[-1].indice == 1 and Variaveis_globais.grupo_players[-1].real:
                estado_player2 = True
                player2 = -1

    # para movimentar o jogador 1
    if estado_player1:


        if pygame.key.get_pressed()[K_a]:
            Variaveis_globais.grupo_players[player1].posicao_x -= velocidade_ia

        if pygame.key.get_pressed()[K_d]:
            Variaveis_globais.grupo_players[player1].posicao_x += velocidade_ia

        if pygame.key.get_pressed()[K_w]:
            Variaveis_globais.grupo_players[player1].posicao_y -= velocidade_ia

        if pygame.key.get_pressed()[K_s]:
            Variaveis_globais.grupo_players[player1].posicao_y += velocidade_ia

    # para movimentar o jogador 2
    if estado_player2:

        if pygame.key.get_pressed()[K_LEFT]:
            Variaveis_globais.grupo_players[player2].posicao_x -= velocidade_ia

        if pygame.key.get_pressed()[K_RIGHT]:
            Variaveis_globais.grupo_players[player2].posicao_x += velocidade_ia

        if pygame.key.get_pressed()[K_UP]:
            Variaveis_globais.grupo_players[player2].posicao_y -= velocidade_ia

        if pygame.key.get_pressed()[K_DOWN]:
            Variaveis_globais.grupo_players[player2].posicao_y += velocidade_ia



# cria os objetos iniciais
criar_objetos(numero_projeteis, numero_players)

# cria classe de colisões
colisoes = Colisoes()

