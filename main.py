from Config import *
import Variaveis_globais as Variaveis_globais
from Jogo.Projeteis import *
from Rede_Neural.Criação_de_Rede import *
from Rede_Neural.Processador import *
from Rede_Neural.Player import *
from Jogo.Colisões import *


# função para criar os objetos
def criar_objetos(quantidade_inimigos, quantidade_playes):   

    # cria os projeteis a partir do valor definido em Config
    for i in range(quantidade_inimigos):

        projetil = Inimigo()
        Variaveis_globais.grupo_inimigos.append(projetil)


    # cria os players a partir do valor definido em Config
    for indice_do_player_na_geracao in range(quantidade_playes):
        
        # se for o inicio de uma nova geração ele cria a nova geração normalmente
        if Variaveis_globais.partida_atual_da_geracao == 0:

            # cria a rede para processar as entradas
            nova_rede = CriarRedeNeural()
            resultado = nova_rede.randomizar_resultados()
            processador = Processador(indice_do_player_na_geracao, *resultado)     
            
            # cria o player, que vai aparecer na tela
            player = Player(False, indice_do_player_na_geracao)

            indice_do_player_na_geracao += 1

            # adiciona a rede e o player em uma lista
            Variaveis_globais.grupo_processadores.append(processador)
            Variaveis_globais.grupo_players.append(player)

        # se não, copia as redes daquela geração
        else:
            processador = Processador(indice_do_player_na_geracao, *Variaveis_globais.geracao_atual[indice_do_player_na_geracao][1:])

            player = Player(False, indice_do_player_na_geracao)

            # adiciona do grupo de redes e players novamente
            Variaveis_globais.grupo_processadores.append(processador)
            Variaveis_globais.grupo_players.append(player)
    
    # condição para adicionar um player para o jogador
    if partida_com_jogador == True:
        player = Player(True, 0)
        Variaveis_globais.grupo_players.append(player)

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

    for inimigo in Variaveis_globais.grupo_inimigos:
        inimigo.update()

    for processador in Variaveis_globais.grupo_processadores:
        processador.update()

    for player in Variaveis_globais.grupo_players:
        player.update()

    # confere as colisões
    colisoes.update()

# função para criar uma nova geração
def nova_geracao():
        
        # zera algumas variaveis que serão usadas a frente
        Variaveis_globais.juncao_de_geracoes = []     
        Variaveis_globais.valores_proporcionais = []
        Variaveis_globais.primeiro_inimigo = 0
        Variaveis_globais.grupo_inimigos = []
       
        # divide a recompensa pela quantidade de partidas para fazer a media de recompensa 
        for individuo in range(numero_players):
            Variaveis_globais.geracao_atual[individuo][0][0] /= partidas_por_geracao

            # confere se existe um novo melhor individuo
            if Variaveis_globais.geracao_atual[individuo][0][0] > Variaveis_globais.melhor_tempo:
                Variaveis_globais.melhor_tempo = Variaveis_globais.geracao_atual[individuo][0][0]
                Variaveis_globais.melhor_individuo = Variaveis_globais.geracao_atual[individuo][1:]

                # se sim, adiciona ele em um arquivo csv
                arquivo = pandas.DataFrame(Variaveis_globais.melhor_individuo)
                arquivo.to_csv('melhor_individuo.csv', index=False)
            
        # printa o melhor tempo
        print(f'melhor tempo {Variaveis_globais.melhor_tempo}')

        # pega a geração atual e passa ela para as gerações passadas, se for a primeira, duplica ela
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

            # adiciona o valor do primeiro individuo normalmente
            if individuo == 0:
                Variaveis_globais.valores_proporcionais.append(Variaveis_globais.juncao_de_geracoes[individuo][0][0] / total_de_recompesa)

                # soma o valor anterior com o do individuo (para manter os valores "progredindo")
            else:
                Variaveis_globais.valores_proporcionais.append(Variaveis_globais.valores_proporcionais[-1] +
                                             Variaveis_globais.juncao_de_geracoes[individuo][0][0] / total_de_recompesa)
                      
       
        # zera a geração atual para ser preenchida novamente
        Variaveis_globais.geracao_atual = []

        # recria a estrutura da geração atual (vazia)
        for individuo in range(numero_players):
            Variaveis_globais.geracao_atual.append([])

        # zera variaveis que vão ser usadas depois
        Variaveis_globais.primeiro_individuo = 0
        Variaveis_globais.ja_sorteados = []

        # cria ou recria os objetos
        criar_objetos(numero_inimigos, numero_players)

def nova_geracao_ou_nova_partida():

    # registra a conclusão de uma partida
    Variaveis_globais.partida_atual_da_geracao += 1

    # confere se a quantidade escolhida de partidas por geração foi completa, se sim, cria a nova geração normalmente
    if Variaveis_globais.partida_atual_da_geracao == partidas_por_geracao:

        # registra que uma geração foi completa
        Variaveis_globais.contador_geracoes += 1
        Variaveis_globais.partida_atual_da_geracao = 0

        # chama a função de criar uma nova geração
        nova_geracao()

    else:
        # zera a variavel que ajuda a eliminar os piores players
        Variaveis_globais.primeiro_inimigo = 0

        # zera os inimigos e recria todos a frente
        Variaveis_globais.grupo_inimigos = []

        criar_objetos(numero_inimigos, numero_players)

# cria os objetos iniciais
criar_objetos(numero_inimigos, numero_players)

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
        
        # verificações para ,ovimentar o player do jogador
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[K_a]:
                Variaveis_globais.comandos[0] = True     

            if pygame.key.get_pressed()[K_d]:
                Variaveis_globais.comandos[1] = True
          
            if pygame.key.get_pressed()[K_w]:
                Variaveis_globais.comandos[2] = True        

            if pygame.key.get_pressed()[K_s]:
                Variaveis_globais.comandos[3] = True       
        
        # verificações para parar de movimentar o jogodor quando soltar a tecla
        if event.type == pygame.KEYUP:
            if not pygame.key.get_pressed()[K_a]:
                Variaveis_globais.comandos[0] = False

            if not pygame.key.get_pressed()[K_d]:
                Variaveis_globais.comandos[1] = False

            if not pygame.key.get_pressed()[K_w]:
                Variaveis_globais.comandos[2] = False

            if not pygame.key.get_pressed()[K_s]:
                Variaveis_globais.comandos[3] = False


    # se todos os players foram "mortos", cria uma nova geração ou partida
    if len(Variaveis_globais.grupo_players) == 0:
        nova_geracao_ou_nova_partida()
       
    # define um limite de fps
    Variaveis_globais.clock.tick(fps)

    # atualiza e preenche o display de preto
    pygame.display.update()
    tela.fill((000, 000, 000))


