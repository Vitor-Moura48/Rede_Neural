from Configurações.Config import *
import Configurações.Variaveis_globais as Variaveis_globais

class Player:
    def __init__(self, real, indice):

        # indice que o player vai ser colocado na variavel geração atual
        self.indice = indice

        # define se o player é ou não um jogador
        self.real = real

        # variavel para contar a quantidade de loops que o player conseguiu passar
        self.tick = 0

        # define o ponto de spaw do player
        self.posicao_x = 750
        self.posicao_y = 250

        # cria um retandulo de colisão e mostra na tela
        self.rect_player = pygame.Rect((self.posicao_x - 5, self.posicao_y - 5, 10, 10))
        draw.rect(tela, (000, 000, 255), (self.posicao_x - 5, self.posicao_y - 5, 10, 10))  
        
    # pega a quantidade de loops que o player passou e retorna esse valor
    def funcao_de_perda(self):

        '''fim = time.time()
        tempo_normalizado = (fim - self.inicio) / 60'''
        tempo_em_tick = self.tick

        return tempo_em_tick

    # retorna o valor mínimo para ativar o neuronio
    def valor_de_ativacao(self):
        
        # se for sigmoid, o valor mínimo é 0.5
        if funcoes_de_camadas[-2] == 1:
            return 0.5
        
        # se for Relu, o valor mínimo é 0
        elif funcoes_de_camadas[-2] == 2:
            return 0
    
    # atualiza o estado do player a cada geração
    def update(self):
       
        # se não for um jogador, conta os loops e se movimenta a partir dos comandos da sua rede
        if self.real == False:

            # conta os loops
            self.tick += 1

            # se houver a função softmax, controla a direção a partir do quanto a rede "quer" ir para uma direção
            if funcoes_de_camadas[-1] == True:
                self.posicao_x += velocidade_ia * Variaveis_globais.grupo_processadores[Variaveis_globais.grupo_players.index(self)].comandos[0]
                self.posicao_x -= velocidade_ia * Variaveis_globais.grupo_processadores[Variaveis_globais.grupo_players.index(self)].comandos[1]
                self.posicao_y += velocidade_ia * Variaveis_globais.grupo_processadores[Variaveis_globais.grupo_players.index(self)].comandos[2]
                self.posicao_y -= velocidade_ia * Variaveis_globais.grupo_processadores[Variaveis_globais.grupo_players.index(self)].comandos[3]

            # as saidas definem a direção que o player vai tomar
            else:
                valor_de_ativacao = self.valor_de_ativacao()

                if Variaveis_globais.grupo_processadores[Variaveis_globais.grupo_players.index(self)].comandos[0] > valor_de_ativacao:
                    self.posicao_x += velocidade_ia
                                    
                if Variaveis_globais.grupo_processadores[Variaveis_globais.grupo_players.index(self)].comandos[1] > valor_de_ativacao:
                    self.posicao_x -= velocidade_ia
                                     
                if Variaveis_globais.grupo_processadores[Variaveis_globais.grupo_players.index(self)].comandos[2] > valor_de_ativacao:
                    self.posicao_y += velocidade_ia             

                if Variaveis_globais.grupo_processadores[Variaveis_globais.grupo_players.index(self)].comandos[3] > valor_de_ativacao:
                    self.posicao_y -= velocidade_ia
                    
                    
            # cria um retandulo de colisão e mostra na tela
            self.rect_player = pygame.Rect((self.posicao_x - 5, self.posicao_y - 5, 10, 10))
            draw.rect(tela, (000, 000, 255), (self.posicao_x - 5, self.posicao_y - 5, 10, 10))

        # se for um jogador troca a cor do player
        else:          
    
            # cria um retandulo de colisão e mostra na tela
            self.rect_player = pygame.Rect((self.posicao_x - 5, self.posicao_y - 5, 10, 10))
            draw.rect(tela, (000, 255, 000), (self.posicao_x - 5, self.posicao_y - 5, 10, 10))