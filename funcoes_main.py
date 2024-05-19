from Configurações.Config import *
from Jogo import projeteis, player, colisao, visualizador
from Rede_Neural import estrategia_evolutiva

# função para criar os objetos
def criar_objetos():   

    estrategia_evolutiva.gerenciador.nova_partida()

    # define a posiçãao e direção inicial (opcional)
    coordendas_iniciais = [[largura + 20, altura / 2, numpy.radians(180)], [largura / 2, -20, numpy.radians(90)], [-20, altura / 2, 0], [largura / 2, altura + 20, numpy.radians(270)]]
    # cria os projeteis a partir do valor definido em Config
    for i in range(4):
        if i > 0:
            projetil = projeteis.Projeteis()   

        else:
            projetil = projeteis.Projeteis(choice(coordendas_iniciais)) # escolhe um projétil para mirar no centro de pawn (para eliminar os que ficam parados)
        projeteis.grupo_projeteis.append(projetil)

# atualiza todos os objetos
def atualizar_objetos():

    # função para exibir o fps
    visualizador.dados.update()

    for projetil in projeteis.grupo_projeteis:
        projetil.update()

    for agente in estrategia_evolutiva.gerenciador.agentes:
        agente.update()

    # confere as colisões
    colisoes.update()

def finalizar_partida():

    # zera os inimigos e recria todos depois
    projeteis.grupo_projeteis = []
    criar_objetos()  

# função para verificar se o jogador movimentou o player e responder (melhorar depois) ################################# REFAZER
def movimentacao_jogador():
    pass

estrategia_evolutiva.gerenciador = estrategia_evolutiva.GerenciadorNeural(500, 10, 0.4, player.Player)
criar_objetos() # cria os objetos iniciais

colisoes = colisao.Colisoes() # cria classe de colisões
visualizador.dados = visualizador.Visualizador()

