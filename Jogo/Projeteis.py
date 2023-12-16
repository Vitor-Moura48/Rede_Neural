from Configurações.Config import *
import Configurações.Variaveis_globais as Variaveis_globais

class Projeteis:  # classe que gerencia os projeteis
    def __init__(self):
    
        # cria dois projeteis na direção do spaw do projetil (para eliminar os que não se movem)
        if Variaveis_globais.primeiro_inimigo == 0:
            self.posicao_x = -20
            self.posicao_y = 245
            self.angulo = numpy.radians(0)
            self.seno = numpy.sin(self.angulo)
            self.coseno = numpy.cos(self.angulo)

            Variaveis_globais.primeiro_inimigo += 1

        elif Variaveis_globais.primeiro_inimigo == 1:
            self.posicao_x = 745
            self.posicao_y = -20
            self.angulo = numpy.radians(90)
            self.seno = numpy.sin(self.angulo)
            self.coseno = numpy.cos(self.angulo)
            Variaveis_globais.primeiro_inimigo += 1

        # spaw padrão dos projeteis
        else:
          self.spaw()

    # função para tornar aleatorio a direção e ponto de partida dos projeteis
    def spaw(self):

        # randomiza se o spaw vai ser "esqueda/direita" ou "cima/baixo"
        self.configuracao = choice([1, 2])

        # se for "esquerda/direita", define qual dos dois lados
        if self.configuracao == 1:
            self.posicao_x = choice([-20, 1520])

            # define um ponto no eixo eixo y aleatório
            self.posicao_y = randint(20, 480)
            
            # escolhe um ângulo de direção de acordo com o lado escolhido e calcula o seno e coseno
            if self.posicao_x == -20:
                self.angulo = choice([numpy.radians(randint(0, 60)), numpy.radians(randint(300, 360))])
                self.seno = numpy.sin(self.angulo)
                self.coseno = numpy.cos(self.angulo)
            else:
                self.angulo = numpy.radians(randint(120, 240))
                self.seno = numpy.sin(self.angulo)
                self.coseno = numpy.cos(self.angulo)

        # se "cima/baixo", define qual dos dois lados
        else:
            self.posicao_y = choice([-20, 520])

            # define um ponto no eixo x aleatório
            self.posicao_x = randint(20, 1480)

            # escolhe um ângulo de direção de acordo com o lado escolhido e calcula o seno e coseno
            if self.posicao_y == -20:
                self.angulo = numpy.radians(randint(30, 150))
                self.seno = math.sin(self.angulo)
                self.coseno = math.cos(self.angulo)
            else:
                self.angulo = numpy.radians(randint(210, 330))
                self.seno = math.sin(self.angulo)
                self.coseno = math.cos(self.angulo)


    # função que retorna algumas informações do projetil (usado no processamento da rede)
    def informar_posicao(self):
        direcao_x_do_projetil = self.coseno
        direcao_y_do_projetil = self.seno
        return self.rect.center[0], self.rect.center[1], direcao_x_do_projetil, direcao_y_do_projetil

    # atualiza estado a cada iteração
    def update(self):

        # respawna os projeteis quando saem da área
        if self.posicao_x < -60 or self.posicao_x > 1560 or self.posicao_y < -60 or self.posicao_y > 560:
            self.spaw()

        # faz a movimentação dos projeteis
        self.posicao_x += velocidade_projetil * self.coseno
        self.posicao_y += velocidade_projetil * self.seno

        # cria um retandulo de colisão e mostra na tela
        self.rect = pygame.Rect((self.posicao_x, self.posicao_y, dimensoes_projetil[0], dimensoes_projetil[1]))
        pygame.draw.rect(tela, (255, 000, 000), (self.posicao_x, self.posicao_y, dimensoes_projetil[0], dimensoes_projetil[1]))

