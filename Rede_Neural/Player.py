from Configurações.Config import *
import Configurações.Global as Global

class Player:
    def __init__(self, real, indice):

        # indice que o player vai ser colocado na variavel geração atual
        self.indice = indice

        # define se o player é ou não um jogador
        self.real = real

        # variavel para contar a quantidade de loops que o player conseguiu passar
        self.tick = 0

        # define o ponto de spaw do player
        self.posicao_x = largura / 2
        self.posicao_y = altura / 2

        self.valor_de_ativacao = self.valor_de_ativacao()

        # cria um retandulo de colisão e mostra na tela
        self.rect = pygame.Rect((self.posicao_x, self.posicao_y, dimensoes_rede[0], dimensoes_rede[1]))
     
    # retorna o valor mínimo para ativar o neuronio
    def valor_de_ativacao(self):
        
        # se for sigmoid, o valor mínimo é 0.5
        if funcoes_de_camadas[-2] == 1:
            return 0.5
        
        # se for Relu, o valor mínimo é 0
        elif funcoes_de_camadas[-2] == 2:
            return 0
        
        # se for Tangente Hiperbólica, o valor mínimo é 0
        elif funcoes_de_camadas[-2] == 3:
            return 0
    
    # atualiza o estado do player a cada geração
    def update(self):
       
        # se não for um jogador, conta os loops e se movimenta a partir dos comandos da sua rede
        if self.real == False:

            # conta os loops
            self.tick += 1

            # se houver a função softmax, controla a direção a partir do quanto a rede "quer" ir para uma direção
            if funcoes_de_camadas[-1] == True:
                self.posicao_x += velocidade_ia * (Global.grupo_processadores[self.indice].comandos[0] - Global.grupo_processadores[self.indice].comandos[1])
                self.posicao_y += velocidade_ia * (Global.grupo_processadores[self.indice].comandos[2] - Global.grupo_processadores[self.indice].comandos[3])

            # as saidas definem a direção que o player vai tomar
            else:

                if Global.grupo_processadores[self.indice].comandos[0] > self.valor_de_ativacao:
                    self.posicao_x += velocidade_ia
                                    
                if Global.grupo_processadores[self.indice].comandos[1] > self.valor_de_ativacao:
                    self.posicao_x -= velocidade_ia
                                     
                if Global.grupo_processadores[self.indice].comandos[2] > self.valor_de_ativacao:
                    self.posicao_y += velocidade_ia             

                if Global.grupo_processadores[self.indice].comandos[3] > self.valor_de_ativacao:
                    self.posicao_y -= velocidade_ia
                    
                    
            # cria um retandulo de colisão e mostra na tela
            self.rect.center = (self.posicao_x, self.posicao_y)
            draw.rect(tela, (000, 000, 255), self.rect)
            draw.rect(tela, (000, 255, 000), self.rect, 2)

        # se for um jogador troca a cor do player
        else:          
    
            # cria um retandulo de colisão e mostra na tela
            self.rect.center = (self.posicao_x, self.posicao_y)
            draw.rect(tela, (000, 255, 000), (self.posicao_x - 5, self.posicao_y - 5, dimensoes_rede[0], dimensoes_rede[1]))