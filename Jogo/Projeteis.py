from Config import *
import Variaveis_globais as Variaveis_globais

class Inimigo:  # classe que gerencia os inimigos
    def __init__(self):
    
        # cria dois projeteis na direção do spaw do inimigo
        if Variaveis_globais.primeiro_inimigo == 0:
            self.posicao_x = -20
            self.posicao_y = 245
            self.angulo = numpy.radians(0)
            self.seno = numpy.sin(self.angulo)
            self.coseno = numpy.cos(self.angulo)
            self.configuracao = 1

            Variaveis_globais.primeiro_inimigo += 1
        elif Variaveis_globais.primeiro_inimigo == 1:
            self.posicao_x = 745
            self.posicao_y = -20
            self.angulo = numpy.radians(270)
            self.seno = numpy.sin(self.angulo)
            self.coseno = numpy.cos(self.angulo)
            self.configuracao = 2
            Variaveis_globais.primeiro_inimigo += 1

        # spaw padrão dos inimigos
        else:
          self.spaw()

    # função para tornar aleatorio a direção e ponto de partida dos inimigos
    def spaw(self):
        global tela

        # randomiza o spaw dos inimigos
        self.configuracao = choice([1, 2])

        if self.configuracao == 1:
            self.posicao_x = choice([-20, 1520])
            self.posicao_y = randint(20, 480)
            
            if self.posicao_x == -20:
                self.angulo = choice([numpy.radians(randint(0, 60)), numpy.radians(randint(300, 360))])
                self.seno = numpy.sin(self.angulo)
                self.coseno = numpy.cos(self.angulo)
            else:
                self.angulo = numpy.radians(randint(120, 240))
                self.seno = numpy.sin(self.angulo)
                self.coseno = numpy.cos(self.angulo)


        else:
            self.posicao_y = choice([-20, 520])
            self.posicao_x = randint(20, 1480)

            if self.posicao_y == -20:
                self.angulo = numpy.radians(randint(210, 330))
                self.seno = math.sin(self.angulo)
                self.coseno = math.cos(self.angulo)
            else:
                self.angulo = numpy.radians(randint(30, 150))
                self.seno = math.sin(self.angulo)
                self.coseno = math.cos(self.angulo)
    
    

    # informa a posição do inimigo para calcular a distancia entre os individuos e os inimigos
    def informar_posicao(self):
        direcao_x_do_projetil = self.coseno
        direcao_y_do_projetil = self.seno
        return self.rect_inimigo.center[0], self.rect_inimigo.center[1], direcao_x_do_projetil, direcao_y_do_projetil

    # atualiza estado
    def update(self):
        # respawna os inimigos quando saem da área
        if self.posicao_x < -60 or self.posicao_x > 1560 or self.posicao_y < -60 or self.posicao_y > 560:
            self.spaw()

        # define a movimentação inimiga
        if self.configuracao == 1:
            self.posicao_x += velocidade_projetil * self.coseno
            self.posicao_y += velocidade_projetil * self.seno

        if self.configuracao == 2:
            self.posicao_x += velocidade_projetil * self.coseno
            self.posicao_y -= velocidade_projetil * self.seno

        # cria um retandulo de colisão e mostra na tela
        self.rect_inimigo = pygame.Rect((self.posicao_x, self.posicao_y, 10, 10))
        pygame.draw.rect(tela, (255, 000, 000), (self.posicao_x, self.posicao_y, 10, 10))

