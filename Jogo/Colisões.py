from Config import *
import Variaveis_globais as Variaveis_globais

class Colisoes:
    def __init__(self):
        pass

    # função para conferir as colisões com o player
    def colisao_player_inimigo(self):

        # para evitar que um individuo seja atingido por um inimigo e saia do limite da tela ao mesmo tempo (daria erro)
        self.colidiu = False

        # confere se cada inimigo colidiu com o player
        for player in Variaveis_globais.grupo_players:
            for inimigo in Variaveis_globais.grupo_inimigos:
              
                if player.rect_player.colliderect(inimigo.rect_inimigo):
                
   
                    # se sim, vai remover o player do grupo de players
                    Variaveis_globais.grupo_players.remove(player)

                    # obter o tempo de vida do individuo
                    tempo_de_vida = player.funcao_de_perda()

                    # enviar os pesos do individuo para a lista da geração
                    pesos_individuo = []
                    pesos_individuo.append([tempo_de_vida])
                    for camada in player.camadas:
                        pesos_individuo.append(camada)

                    Variaveis_globais.geracao_atual.append(pesos_individuo)

                    # se o tempo de vida dele for maior que o do melhor individuo, ele se torna o melhor
                    if tempo_de_vida > Variaveis_globais.melhor_tempo:
                        Variaveis_globais.melhor_tempo = tempo_de_vida
                        Variaveis_globais.melhor_individuo = player.camadas
                        

                    # avisa que o player já colidiu
                    self.colidiu = True

                    # se um inimigo já tiver colidido, não é mais necessario fazer mais verificações
                    break

    def colisao_player_tela(self):

        # confere se o player saiu dos limites da tela
        for player in Variaveis_globais.grupo_players:
            if player.rect_player.bottom < 0 or player.rect_player.top > altura or \
                    player.rect_player.left < 0 or player.rect_player.right > largura and not self.colidiu:

                # se saiu, faz a mesma coisa da colisão com um inimigo
                if player in Variaveis_globais.grupo_players:
                    Variaveis_globais.grupo_players.remove(player)

                    # pune os individuos que colidiram com a tela
                    tempo_de_vida = player.funcao_de_perda() - 1000

                    pesos_individuo = []
                    pesos_individuo.append([tempo_de_vida])
                    for camada in player.camadas:
                        pesos_individuo.append(camada)
                    

                    Variaveis_globais.geracao_atual.append(pesos_individuo)

                    # so vai para "pódio" de melhor individuo se for pelo menos 10% melhor que o atual melhor
                    if tempo_de_vida > Variaveis_globais.melhor_tempo:
                        Variaveis_globais.melhor_tempo = tempo_de_vida
                        Variaveis_globais.melhor_individuo = player.camadas
                        

    def update(self):
        self.colisao_player_inimigo()
        self.colisao_player_tela()

