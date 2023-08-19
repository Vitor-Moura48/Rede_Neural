from Config import *
import Variaveis_globais as Variaveis_globais

class Player:
    def __init__(self, real, indice, *args):

        # indice que o player vai ser colocado na variavel geração atual
        self.indice = indice

        self.real = real

         # variavel para contar a quantidade de loops que o player conseguiu passar
        self.tick = 0
        
    # pega a quantidade de loops que o player passou e retorna esse valor
    def funcao_de_perda(self):

        '''fim = time.time()
        tempo_normalizado = (fim - self.inicio) / 60'''
        tempo_em_tick = self.tick

        return tempo_em_tick
    
    
    def update(self):
       
         # conta os loops
        self.tick += 1

        # as saidas definem a direção que o player vai tomar
        if processamentos_da_rede[-1][0] > 0:
            self.posicao_x += velocidade_ia
        if processamentos_da_rede[-1][1] > 0:
            self.posicao_x -= velocidade_ia

        if processamentos_da_rede[-1][2] > 0:
            self.posicao_y += velocidade_ia
        if processamentos_da_rede[-1][3] > 0:
            self.posicao_y -= velocidade_ia
        
        # cria um retandulo de colisão e mostra na tela
        self.rect_player = pygame.Rect((self.posicao_x - 5, self.posicao_y - 5, 10, 10))
        draw.rect(tela, (000, 000, 255), (self.posicao_x - 5, self.posicao_y - 5, 10, 10))  
