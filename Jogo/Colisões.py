from Configurações.Config import *
import Configurações.Variaveis_globais as Variaveis_globais

#classe para conferir conliões
class Colisoes:
    def __init__(self):
        pass

    # função para conferir as colisões com o player
    def verificar_colisao(self):

        # confere se cada player colidiu com cada inimigo
        for player in Variaveis_globais.grupo_players:
            if player.rect_player.collidelist([projetil.rect_inimigo for projetil in Variaveis_globais.grupo_projeteis]) != -1 or \
            player.rect_player.bottom < 0 or player.rect_player.top > altura or player.rect_player.left < 0 or player.rect_player.right > largura:

                # se colidiu e não for o jogador:
                if player.real == False:
                
                    # obtem o tempo de vida do individuo
                    tempo_de_vida = player.funcao_de_perda()

                    # se for a primeira partida de geração, preenche a a lista de geração_atual
                    if Variaveis_globais.partida_atual_da_geracao == 0:
                    
                        # junta o tempo de vida e os pesos da rede em uma lista e coloca os pesos do individuo no indice escolhido no inicio da geração
                        Variaveis_globais.geracao_atual[player.indice] = [[tempo_de_vida]] + Variaveis_globais.grupo_processadores[Variaveis_globais.grupo_players.index(player)].camadas

                    # se não for a primeira partida, apenas incrementa o valor (para tirar a média no futuro)
                    else:
                        Variaveis_globais.geracao_atual[player.indice][0][0] += tempo_de_vida

                    # apaga a rede da lista de redes (se não for o própio jogador)
                    Variaveis_globais.grupo_processadores.pop(Variaveis_globais.grupo_players.index(player))   
                
                # apaga o player da lista de players
                Variaveis_globais.grupo_players.pop(Variaveis_globais.grupo_players.index(player))
                        
    # função para chamar as funções de colisão a cada iteração
    def update(self):
        self.verificar_colisao()

