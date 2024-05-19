from Configurações.Config import *
import Configurações.Global as Global

class Projeteis:  # classe que gerencia os projeteis
    def __init__(self, *args):
        
        # se tiver argumentos (provavelmente é de posição e diração)
        if len(args) > 0:
            self.posicao_x = args[0][0]
            self.posicao_y = args[0][1]
            self.seno = numpy.sin(args[0][2])
            self.coseno = numpy.cos(args[0][2])

        # spawn padrão
        else:
            self.spawn()
        
        self.rect = pygame.Rect((self.posicao_x, self.posicao_y, dimensoes_projetil[0], dimensoes_projetil[1]))

    # função para tornar aleatorio a direção e ponto de partida dos projeteis
    def spawn(self):

        # randomiza se o spawn vai ser "esqueda/direita" ou "cima/baixo"
        self.configuracao = choice([1, 2])

        # se for "esquerda/direita", define qual dos dois lados
        if self.configuracao == 1:
            self.posicao_x = choice([-20, largura + 20])

            # define um ponto no eixo eixo y aleatório
            self.posicao_y = randint(-20, altura + 20)
            
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
            self.posicao_y = choice([-20, altura + 20])

            # define um ponto no eixo x aleatório
            self.posicao_x = randint(-20, largura + 20)

            # escolhe um ângulo de direção de acordo com o lado escolhido e calcula o seno e coseno
            if self.posicao_y == -20:
                self.angulo = numpy.radians(randint(30, 150))
                self.seno = numpy.sin(self.angulo)
                self.coseno = numpy.cos(self.angulo)
            else:
                self.angulo = numpy.radians(randint(210, 330))
                self.seno = numpy.sin(self.angulo)
                self.coseno = numpy.cos(self.angulo)

    # função que retorna algumas informações do projetil (usado no processamento da rede)
    def informar_posicao(self):
        return self.rect.center[0], self.rect.center[1], self.coseno, self.seno

    # atualiza estado a cada iteração
    def update(self):

        # faz a movimentação dos projeteis
        self.posicao_x += velocidade_projetil * self.coseno
        self.posicao_y += velocidade_projetil * self.seno

        # respawna os projeteis quando saem da área
        if self.posicao_x < -20 or self.posicao_x > (largura + 20) or self.posicao_y < -20 or self.posicao_y > altura + 20:
            self.spawn()

        # cria um retandulo de colisão e mostra na tela
        self.rect.center = (self.posicao_x, self.posicao_y)
        pygame.draw.rect(tela, (255, 000, 000), self.rect)
    
grupo_projeteis = []

        

        

        

