from Config import *
from Criação_de_Rede import*

# classe que gerencia o player
class Player:
    def __init__(self):
        global contador_geracoes, melhor_peso_primeira_camada_oculta, melhor_peso_camada_de_saida, primeiro_individuo, \
                juncao_de_geracoes, ja_sorteados
        
        nova_rede = CriarRedeNeural()
        self.grupo_neuronios_primeira_camada_oculta, self.grupo_neuronios_camada_de_saida = nova_rede.obter_resultado()
        

        # variavel para contar a quantidade de loops que o player conseguiu passar
        self.tick = 0

        # define o valor do vies da rede neural
        self.bias = 1

         # define o ponto de spaw do player
        self.posicao_x = 750
        self.posicao_y = 250

        # cria um retandulo de colisão e mostra na tela
        self.rect_player = pygame.Rect((self.posicao_x - 5, self.posicao_y - 5, 10, 10))
        draw.rect(tela, (000, 000, 255), (self.posicao_x - 5, self.posicao_y - 5, 10, 10))

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
        
        # cria um retandulo de colisão e mostra na tela
        self.rect_player = pygame.Rect((self.posicao_x - 5, self.posicao_y - 5, 10, 10))
        draw.rect(tela, (000, 000, 255), (self.posicao_x - 5, self.posicao_y - 5, 10, 10))  
