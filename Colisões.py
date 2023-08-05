from Config import *

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
