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
    
    # atualiza o estado do player a cada geração
    def update(self):
       
        # se não for um jogador, conta os loops e se movimenta a partir dos comandos da sua rede
        if self.real == False:

            # conta os loops
            self.tick += 1

            # as saidas definem a direção que o player vai tomar
            if Variaveis_globais.grupo_processadores[Variaveis_globais.grupo_players.index(self)].comandos[0] > 0:
                self.posicao_x += velocidade_ia
            if Variaveis_globais.grupo_processadores[Variaveis_globais.grupo_players.index(self)].comandos[1] > 0:
                self.posicao_x -= velocidade_ia

            if Variaveis_globais.grupo_processadores[Variaveis_globais.grupo_players.index(self)].comandos[2] > 0:
                self.posicao_y += velocidade_ia
            if Variaveis_globais.grupo_processadores[Variaveis_globais.grupo_players.index(self)].comandos[3] > 0:
                self.posicao_y -= velocidade_ia
            
            # cria um retandulo de colisão e mostra na tela
            self.rect_player = pygame.Rect((self.posicao_x - 5, self.posicao_y - 5, 10, 10))
            draw.rect(tela, (000, 000, 255), (self.posicao_x - 5, self.posicao_y - 5, 10, 10))

        # se for um jogador troca a cor do player
        else:          
    
            # cria um retandulo de colisão e mostra na tela
            self.rect_player = pygame.Rect((self.posicao_x - 5, self.posicao_y - 5, 10, 10))
            draw.rect(tela, (000, 255, 000), (self.posicao_x - 5, self.posicao_y - 5, 10, 10))