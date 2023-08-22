from Config import *
import Variaveis_globais as Variaveis_globais

#classe para conferir conliões
class Colisoes:
    def __init__(self):
        pass

    # função para conferir as colisões com o player
    def colisao_player_inimigo(self):

        # para evitar que um individuo seja atingido por um inimigo e saia do limite da tela ao mesmo tempo
        self.colidiu = False

        # confere se cada player colidiu com cada inimigo
        for player in Variaveis_globais.grupo_players:
            for inimigo in Variaveis_globais.grupo_projeteis:
              
                if player.rect_player.colliderect(inimigo.rect_inimigo):

                    # se colidiu e não for o jogador:
                    if player.real == False:
                    
                        # obtem o tempo de vida do individuo
                        tempo_de_vida = player.funcao_de_perda()

                        # se for a primeira partida de geração, preenche a a lista de geração_atual
                        if Variaveis_globais.partida_atual_da_geracao == 0:
                        
                            # junta o tempo de dvida e os pesos da rede em uma lista
                            pesos_individuo = []
                            pesos_individuo.append([tempo_de_vida])
                            for camada in Variaveis_globais.grupo_processadores[Variaveis_globais.grupo_players.index(player)].camadas:
                                pesos_individuo.append(camada)

                            # coloca os pesos do individuo no indice escolhido no inicio da geração
                            Variaveis_globais.geracao_atual[player.indice] = pesos_individuo
                        
                        # se não for a primeira partida, apenas incrementa o valor (para tirar a média no futuro)
                        else:
                            Variaveis_globais.geracao_atual[player.indice][0][0] += tempo_de_vida

                        # confirna que o player já colidiu
                        self.colidiu = True
                    
                        # apaga a rede da lista de redes (se não for o própio jogador)
                        Variaveis_globais.grupo_processadores.pop(Variaveis_globais.grupo_players.index(player))   
                    
                    # apaga o player da lista de players
                    Variaveis_globais.grupo_players.pop(Variaveis_globais.grupo_players.index(player))

                    # se um inimigo já tiver colidido, não é mais necessario fazer mais verificações
                    break

    # função para conferir as colisões do player com a tela
    def colisao_player_tela(self):

        # confere cada player, se saiu dos limites da tela
        for player in Variaveis_globais.grupo_players:
            if player.rect_player.bottom < 0 or player.rect_player.top > altura or \
                player.rect_player.left < 0 or player.rect_player.right > largura and not self.colidiu:
                

                # se saiu, faz a mesma coisa da colisão com um inimigo
                if player in Variaveis_globais.grupo_players:

                    if not player.real:
                        
                        # reduz o tempo de vida dos players que colidiram com a tela (para evitar que as próximas redes façam a mesma coisa)
                        tempo_de_vida = player.funcao_de_perda() * 0.8

                        if Variaveis_globais.partida_atual_da_geracao == 0:
                        
                            pesos_individuo = []
                            pesos_individuo.append([tempo_de_vida])
                            for camada in Variaveis_globais.grupo_processadores[Variaveis_globais.grupo_players.index(player)].camadas:
                                pesos_individuo.append(camada)
                            
                            Variaveis_globais.geracao_atual[player.indice] = pesos_individuo

                        else:
                            Variaveis_globais.geracao_atual[player.indice][0][0] += tempo_de_vida
                    
                
                        Variaveis_globais.grupo_processadores.pop(Variaveis_globais.grupo_players.index(player))   
                    
                    Variaveis_globais.grupo_players.pop(Variaveis_globais.grupo_players.index(player))
                        
    # função para chamar as funções de colisão a cada iteração
    def update(self):
        self.colisao_player_inimigo()
        self.colisao_player_tela()

