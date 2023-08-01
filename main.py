import pygame
from pygame import *
import sys
import numpy
from random import *
import math
import time
import copy

# largura e altura da tela
largura = 1500
altura = 500

# inicia o pygame e define um limite de fps
pygame.init()
fps = 120

velocidade_projetil = 6  # 10 max no caso
velocidade_ia = 6  # 9 max no caso (10 inimogo, 10 player) 10 + 9 = 19  -- 20 (10 + 10)

tela = pygame.display.set_mode((largura, altura))
tela.fill((000, 000, 000))

# ajuda a selecionar o melhor individuo de cada geração
melhor_tempo = 0

contador_geracoes = 0

geracao_avo = []
geracao_anterior = []
geracao_atual = []

juncao_de_geracoes = []
valores_proporcionais = []

# variavel para ajudar a direcionar os primeiros projeteis exatamente na direção do surgimento do player, para eliminar os piores
primeiro_inimigo = 0

# variavel para ajudar a manter sempre o melhor player
primeiro_individuo = True


class Inimigo:  # classe que gerencia os inimigos
    def __init__(self):
        global primeiro_inimigo

        # cria dois projeteis na direção do spaw do inimigo
        if primeiro_inimigo == 0:
            self.posicao_x = -20
            self.posicao_y = 245
            self.angulo = numpy.radians(0)
            self.seno = numpy.sin(self.angulo)
            self.coseno = numpy.cos(self.angulo)
            self.configuracao = 1

            primeiro_inimigo += 1
        elif primeiro_inimigo == 1:
            self.posicao_x = 745
            self.posicao_y = -20
            self.angulo = numpy.radians(270)
            self.seno = numpy.sin(self.angulo)
            self.coseno = numpy.cos(self.angulo)
            self.configuracao = 2
            primeiro_inimigo += 1

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
        else:
            self.posicao_y = choice([-20, 520])
            self.posicao_x = randint(20, 1480)

        if self.configuracao == 1:
            if self.posicao_x == -20:
                self.angulo = choice([numpy.radians(randint(0, 60)), numpy.radians(randint(300, 360))])
                self.seno = numpy.sin(self.angulo)
                self.coseno = numpy.cos(self.angulo)
            else:
                self.angulo = numpy.radians(randint(120, 240))
                self.seno = numpy.sin(self.angulo)
                self.coseno = numpy.cos(self.angulo)

        if self.configuracao == 2:
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
        return self.rect_inimigo.center

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
        draw.rect(tela, (255, 000, 000), (self.posicao_x, self.posicao_y, 10, 10))


# classe que gerencia o player
class Player:
    def __init__(self):
        global contador_geracoes, melhor_peso_primeira_camada_oculta, melhor_peso_camada_de_saida, primeiro_individuo, \
                juncao_de_geracoes

        # variavel para contar a quantidade de loops que o player conseguiu passar
        self.tick = 0

        # define o ponto de spaw do player
        self.posicao_x = 750
        self.posicao_y = 250

        # cria um retandulo de colisão e mostra na tela
        self.rect_player = pygame.Rect((self.posicao_x - 5, self.posicao_y - 5, 10, 10))
        draw.rect(tela, (000, 000, 255), (self.posicao_x - 5, self.posicao_y - 5, 10, 10))

        # define o valor do vies da rede neural
        self.bias = 1

        # se for a primeira geração ele cria os pesos e randomiza-os
        if contador_geracoes == 0:

            self.grupo_neuronios_primeira_camada_oculta = []  # pesos da camada de entrada para a primeira camada oculta

            pesos_para_primeiro_neuronio_da_primeira_camada_oculta = numpy.array([0] * 19, dtype=float)
            self.grupo_neuronios_primeira_camada_oculta.append(pesos_para_primeiro_neuronio_da_primeira_camada_oculta)

            pesos_para_segundo_neuronio_da_primeira_camada_oculta = numpy.array([0] * 19, dtype=float)
            self.grupo_neuronios_primeira_camada_oculta.append(pesos_para_segundo_neuronio_da_primeira_camada_oculta)

            pesos_para_terceiro_neuronio_da_primeira_camada_oculta = numpy.array([0] * 19, dtype=float)
            self.grupo_neuronios_primeira_camada_oculta.append(pesos_para_terceiro_neuronio_da_primeira_camada_oculta)

            pesos_para_quarto_neuronio_da_primeira_camada_oculta = numpy.array([0] * 19, dtype=float)
            self.grupo_neuronios_primeira_camada_oculta.append(pesos_para_quarto_neuronio_da_primeira_camada_oculta)

            pesos_para_quinto_neuronio_da_primeira_camada_oculta = numpy.array([0] * 19, dtype=float)
            self.grupo_neuronios_primeira_camada_oculta.append(pesos_para_quinto_neuronio_da_primeira_camada_oculta)

            self.grupo_neuronios_camada_de_saida = []  # pesos da primeira camada oculta para a camada de saida

            pesos_para_primeiro_neuronio_da_camada_de_saida = numpy.array([0] * 5, dtype=float)
            self.grupo_neuronios_camada_de_saida.append(pesos_para_primeiro_neuronio_da_camada_de_saida)

            pesos_para_segundo_neuronio_da_camada_de_saida = numpy.array([0] * 5, dtype=float)
            self.grupo_neuronios_camada_de_saida.append(pesos_para_segundo_neuronio_da_camada_de_saida)

            pesos_para_terceiro_neuronio_da_camada_de_saida = numpy.array([0] * 5, dtype=float)
            self.grupo_neuronios_camada_de_saida.append(pesos_para_terceiro_neuronio_da_camada_de_saida)

            pesos_para_quarto_neuronio_da_camada_de_saida = numpy.array([0] * 5, dtype=float)
            self.grupo_neuronios_camada_de_saida.append(pesos_para_quarto_neuronio_da_camada_de_saida)

            # randomizando cada peso
            for neuronio in range(len(self.grupo_neuronios_primeira_camada_oculta)):
                for peso in range(19):
                    self.grupo_neuronios_primeira_camada_oculta[neuronio][peso] = round(uniform(-5, 5), 6)
                self.grupo_neuronios_primeira_camada_oculta[neuronio][-1] = self.bias

            for neuronio in range(len(self.grupo_neuronios_camada_de_saida)):
                for peso in range(5):
                    self.grupo_neuronios_camada_de_saida[neuronio][peso] = round(uniform(-5, 5), 6)
                self.grupo_neuronios_camada_de_saida[neuronio][-1] = self.bias

        # caso não for a primeira geração, ele faz uma nova a partir da(s) anterior(es)
        else:

            # o melhor individuo sempre será passa do para a próxima geração
            if primeiro_individuo:
                self.grupo_neuronios_primeira_camada_oculta = copy.deepcopy(melhor_peso_primeira_camada_oculta)
                self.grupo_neuronios_camada_de_saida = copy.deepcopy(melhor_peso_camada_de_saida)

                # percorre cada neuronio e cada peso do neuronio e randomiza-os
                for neuronio in range(len(self.grupo_neuronios_primeira_camada_oculta)):

                    for peso in range(len(self.grupo_neuronios_primeira_camada_oculta[neuronio])):
                        if randint(1, 10) == 1:
                            self.grupo_neuronios_primeira_camada_oculta[neuronio][peso] = \
                            round(uniform(self.grupo_neuronios_primeira_camada_oculta[neuronio][peso] - 1,
                                          self.grupo_neuronios_primeira_camada_oculta[neuronio][peso] + 1), 8)

                for neuronio in range(len(self.grupo_neuronios_camada_de_saida)):
                    for peso in range(len(self.grupo_neuronios_camada_de_saida[neuronio])):
                        if randint(1, 10) == 1:
                            self.grupo_neuronios_camada_de_saida[neuronio][peso] = \
                                round(uniform(self.grupo_neuronios_camada_de_saida[neuronio][peso] - 1,
                                        self.grupo_neuronios_camada_de_saida[neuronio][peso] + 1), 8)

                primeiro_individuo = False

            # faz um sorteio dos individuos com preferencia dos melhores
            else:

                self.ja_sorteados = []

                # função que sorteia os individuos que ainda não foram sorteados
                def roleta():

                    roleta = uniform(0, 1)
                    primeiro = 0
                    ultimo = len(valores_proporcionais) - 1
                    meio = (primeiro + ultimo) // 2

                    # faz uma busca binaria do individuo sorteado
                    while True:

                        if meio == 0 or meio == ultimo or (roleta > valores_proporcionais[meio - 1] and
                            roleta < valores_proporcionais[meio + 1] and meio not in self.ja_sorteados):

                            self.ja_sorteados.append(meio)
                            break

                        elif roleta > valores_proporcionais[meio]:
                            primeiro = meio + 1
                            meio = (primeiro + ultimo) // 2
                        else:
                            ultimo = meio - 1
                            meio = (primeiro + ultimo) // 2

                    return meio

                # sorteia dois individuos
                roleta_1 = roleta()
                roleta_2 = roleta()

                novo_individuo = [[], []]

                # junta caracteristicas dos dois individuos para formar o novo individuo
                camada = randint(1, 2)

                if camada == 1:

                    neuronio = randint(0, 18)


                    novo_individuo[0] = juncao_de_geracoes[roleta_1][1][:neuronio + 1]
                    if neuronio != 18:
                        novo_individuo[0] += juncao_de_geracoes[roleta_2][1][neuronio + 1:]


                    novo_individuo[1] = juncao_de_geracoes[roleta_2][2]

                elif camada == 2:
                    neuronio = randint(0, 4)

                    novo_individuo[0] = juncao_de_geracoes[roleta_1][1]

                    novo_individuo[1] = juncao_de_geracoes[roleta_1][2][:neuronio + 1]
                    if neuronio != 4:
                        novo_individuo[1] += juncao_de_geracoes[roleta_2][2][neuronio + 1:]

                # percorre cada neuronio e cada peso do neuronio e randomiza-os
                for neuronio in range(len(novo_individuo[0])):

                    for peso in range(len(novo_individuo[0][neuronio])):
                        if randint(1, 10) == 1:
                            novo_individuo[0][neuronio][peso] = \
                                round(uniform(novo_individuo[0][neuronio][peso] - 1,
                                              novo_individuo[0][neuronio][peso] + 1), 8)

                for neuronio in range(len(novo_individuo[1])):
                    for peso in range(len(novo_individuo[1][neuronio])):
                        if randint(1, 10) == 1:
                            novo_individuo[1][neuronio][peso] = \
                                round(uniform(novo_individuo[1][neuronio][peso] - 1,
                                              novo_individuo[1][neuronio][peso] + 1), 8)

                # adiciona cada conjunto de pesos nas variaveis
                self.grupo_neuronios_primeira_camada_oculta = novo_individuo[0]
                self.grupo_neuronios_camada_de_saida = novo_individuo[1]

    # funções de ativação que posem ser usadas
    def funcao_sigmoide(self, entrada):
        return (1 / 1 + numpy.exp(entrada))

    def funcao_relu(self, entrada):
        if entrada < 0:
            entrada = 0
        return entrada

    # pega a quantidade de loops que o player passou e retorna esse valor
    def funcao_de_perda(self):

        '''fim = time.time()
        tempo_normalizado = (fim - self.inicio) / 60'''
        tempo_em_tick = self.tick

        return tempo_em_tick

    # função para retornar as entradas para a rede neural
    def obter_entradas(self):
        global grupo_inimigos

        # variavel que vai ser retornada após ser tratada
        resultados_sensores = []

        # obtem as distâncias de cada inimigo para o jogador e retorna o valor
        def obter_distancias():
            for inimigo in grupo_inimigos:

                coordenada_inimigo = inimigo.informar_posicao()
                distancia_x = 1 - (abs(coordenada_inimigo[0] - self.rect_player.center[0]) / 110)
                distancia_y = 1 - (abs(coordenada_inimigo[1] - self.rect_player[1]) / 110)

                distancia = (distancia_x ** 2 + distancia_y ** 2) ** 0.5

                resultados_sensores.append([distancia, distancia_x, distancia_y])

        # ordena cada coordenada (dos inimigos) de acordo com os que estão mais próximos
        def ordenar_cada_inimigo():
            resultados_sensores.sort(key=lambda x: x[0])

        # apaga as coordenadas exedentes e apaga a distancia absoluta dos resultados (usada para "ordenar cada inimigo")
        def normatizar_o_resultado():

            while len(resultados_sensores) > 8:
                resultados_sensores.pop(-1)

            for coordenada in range(8):
                resultados_sensores[coordenada].pop(0)

        # chama todas essas funções
        obter_distancias()
        ordenar_cada_inimigo()
        normatizar_o_resultado()

        # retorna as coordenadas mais próximas
        return resultados_sensores

    # atualiza o estado do player
    def update(self):

        # conta os loops
        self.tick += 1

        # cria um retandulo de colisão e mostra na tela
        self.rect_player = pygame.Rect((self.posicao_x - 5, self.posicao_y - 5, 10, 10))
        draw.rect(tela, (000, 000, 255), (self.posicao_x - 5, self.posicao_y - 5, 10, 10))

        # obtem os resultados dos 8 inimigos mais próximos
        resultados = self.obter_entradas()

        # junta todos os dados que vão para a entrada da rede em uma única lista
        juncao = []
        juncao.append(self.bias)
        juncao.append(abs(1 - (self.rect_player.center[0] / 750)))
        juncao.append(abs(1 - (self.rect_player.center[1] / 250)))
        for coordenada in resultados:
            for valor in coordenada:
                juncao.append(valor)

        # vai transformando as listas em arrays, para facilitar os calculos
        entradas_1 = numpy.array(juncao)

        entradas_2 = []
        # faz a soma de todas as entradas com seus respectivos pesos e usa função de ativação para melhorar o  resultado
        camada_oculta_1_neuronoio_1 = self.funcao_relu(sum(entradas_1 * self.grupo_neuronios_primeira_camada_oculta[0]))
        entradas_2.append(camada_oculta_1_neuronoio_1)
        camada_oculta_1_neuronoio_2 = self.funcao_relu(sum(entradas_1 * self.grupo_neuronios_primeira_camada_oculta[1]))
        entradas_2.append(camada_oculta_1_neuronoio_2)
        camada_oculta_1_neuronoio_3 = self.funcao_relu(sum(entradas_1 * self.grupo_neuronios_primeira_camada_oculta[2]))
        entradas_2.append(camada_oculta_1_neuronoio_3)
        camada_oculta_1_neuronoio_4 = self.funcao_relu(sum(entradas_1 * self.grupo_neuronios_primeira_camada_oculta[3]))
        entradas_2.append(camada_oculta_1_neuronoio_4)
        camada_oculta_1_neuronoio_5 = self.funcao_relu(sum(entradas_1 * self.grupo_neuronios_primeira_camada_oculta[4]))
        entradas_2.append(camada_oculta_1_neuronoio_5)

        # vai transformando as listas em arrays, para facilitar os calculos
        entradas_2 = numpy.array(entradas_2)

        # faz os mesmos calculos que a camada acima
        camada_saida_neuronio_1 = self.funcao_relu(sum(entradas_2 * self.grupo_neuronios_camada_de_saida[0]))
        camada_saida_neuronio_2 = self.funcao_relu(sum(entradas_2 * self.grupo_neuronios_camada_de_saida[1]))
        camada_saida_neuronio_3 = self.funcao_relu(sum(entradas_2 * self.grupo_neuronios_camada_de_saida[2]))
        camada_saida_neuronio_4 = self.funcao_relu(sum(entradas_2 * self.grupo_neuronios_camada_de_saida[3]))

        # as saidas definem a direção que o player vai tomar
        if camada_saida_neuronio_1 > 0:
            self.posicao_x += velocidade_ia
        if camada_saida_neuronio_2 > 0:
            self.posicao_x -= velocidade_ia

        if camada_saida_neuronio_3 > 0:
            self.posicao_y += velocidade_ia
        if camada_saida_neuronio_4 > 0:
            self.posicao_y -= velocidade_ia


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


# lista para juntar os objetos das classes
grupo_inimigos = []
grupo_players = []

# cria classe de colisões
colisoes = Colisoes()


# função para criar os objetos
def criar_objetos(quantidade_inimigos, quantidade_playes):

    for i in range(quantidade_inimigos):
        projetil = Inimigo()
        grupo_inimigos.append(projetil)
    for i in range(quantidade_playes):
        player = Player()
        grupo_players.append(player)


# ...
criar_objetos(20, 1500)

# variaveis para ajudar a contar fps
tempo_inicio = time.time()
contador = 0

# cria um limitador de fps
clock = pygame.time.Clock()

# loop principal
while True:

    # lógica para contar o fps
    contador += 1
    tempo_atual = time.time()

    if (tempo_atual - tempo_inicio) > 1:
        print(f'fps {contador}')

        contador = 0
        tempo_inicio = tempo_atual

    # atualiza todos os objetos
    for inimigo in grupo_inimigos:
        inimigo.update()
    for ia in grupo_players:
        ia.update()
    colisoes.update()

    # confere se eu cliquei para sair
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
            sys.exit()

    # se todos os players foram mortos
    if len(grupo_players) == 0:

        # registra que uma geração foi completa
        contador_geracoes += 1

        valores_proporcionais = []

        # zera a variavel que elimina os piores players
        primeiro_inimigo = 0

        # zera os inimigos e recria todos logo a frente
        grupo_inimigos = []

        # printa o melhor tempo
        print(f'melhor tempo {melhor_tempo}')

        # pega a geração atual e passa ela paga as gerações passadas, se for a primeira duplica ela
        if contador_geracoes == 1:
            geracao_avo = geracao_atual
            geracao_anterior = geracao_atual

        else:
            geracao_avo = geracao_anterior
            geracao_anterior = geracao_atual

        # junta as duas gerações mais recentes e organiza os individuos pela recompensa obtida por cada um
        juncao_de_geracoes = geracao_avo + geracao_anterior
        juncao_de_geracoes.sort(key=lambda x: x[0])

        total_de_recompesa = 0

        # soma todas as recompensas dos individuos
        for individuo in range(len(juncao_de_geracoes)):
            total_de_recompesa += int(juncao_de_geracoes[individuo][0][0])

        # adiciona proporcionalmente um valor de acordo com a recompensa de cada individuo (para a roleta)
        for individuo in range(len(juncao_de_geracoes)):
            if individuo == 0:
                valores_proporcionais.append(juncao_de_geracoes[individuo][0][0] / total_de_recompesa)


                # soma o valor anterior com o do individuo (para manter os valores "progredindo")
            else:
                valores_proporcionais.append(valores_proporcionais[-1] +
                                             juncao_de_geracoes[individuo][0][0] / total_de_recompesa)

        # zera a geração atual para ser preenchida novamente
        geracao_atual = []
        primeiro_individuo = True

        criar_objetos(20, 1500)

    # define um limite de fps
    clock.tick(fps)

    # atualiza e preenche o display de preto
    pygame.display.update()
    tela.fill((000, 000, 000))


