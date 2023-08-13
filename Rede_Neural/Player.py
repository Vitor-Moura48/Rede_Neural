from Config import *
import Variaveis_globais as Variaveis_globais


# classe que gerencia o player
class Player:
    def __init__(self, indice, *args):

        # indice que o player vai ser colocado na variavel geração atual
        self.indice = indice
        
        self.camadas = []

        for arg in args:
            self.camadas.append(arg)
        

        # variavel para contar a quantidade de loops que o player conseguiu passar
        self.tick = 0

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

        # variavel que vai ser retornada após ser tratada
        resultados_sensores = []

        # obtem as distâncias de cada inimigo para o jogador e retorna o valor
        def obter_distancias():
            for inimigo in Variaveis_globais.grupo_inimigos:

                informacoes_inimigo = inimigo.informar_posicao()
                distancia_x = 1 - (abs(informacoes_inimigo[0] - self.rect_player.center[0]) / 110)
                distancia_y = 1 - (abs(informacoes_inimigo[1] - self.rect_player[1]) / 110)
            
                distancia = (distancia_x ** 2 + distancia_y ** 2) ** 0.5

                resultados_sensores.append([distancia, distancia_x, distancia_y, informacoes_inimigo[2], informacoes_inimigo[3], velocidade_projetil])

        # ordena cada coordenada (dos inimigos) de acordo com os que estão mais próximos
        def ordenar_cada_inimigo():
            resultados_sensores.sort(key=lambda x: x[0])

        # apaga as coordenadas exedentes e apaga a distancia absoluta dos resultados (usada para "ordenar cada inimigo")
        def normatizar_o_resultado():
            while len(resultados_sensores) > projeteis_para_entrada:
                resultados_sensores.pop(-1)

            for coordenada in range(projeteis_para_entrada):  
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

        # adiciona como entrada a distancia para cada canto da tela
        juncao.append(self.rect_player.center[0] / 1500)
        juncao.append(1 - (self.rect_player.center[0] / 1500))

        juncao.append(self.rect_player.center[1] / 500)
        juncao.append(1 - (self.rect_player.center[1] / 500))
        for coordenada in resultados:
            for valor in coordenada:
                juncao.append(valor)

        # vai transformando as listas em arrays, para facilitar os calculos
        entradas_1 = numpy.array(juncao)

        # armazena o resultado dos calculos de cada neuronios e divide em camadas
        processamentos_da_rede = []
      

        # Faz todos os calculos de cada camada e armazena na variavel acima
        for camada in range(1, len(configuracao_de_camadas)):
            processamento_da_camada = []

            if camada == 1:
                for neuronio in range(configuracao_de_camadas[camada]):
                    processamento_neuronio = self.funcao_relu(sum(entradas_1 * self.camadas[camada - 1][neuronio]))
                    processamento_da_camada.append(processamento_neuronio)             
                
            else:
                for neuronio in range(configuracao_de_camadas[camada]):          
                    processamento_neuronio = self.funcao_relu(sum(processamentos_da_rede[-1] * self.camadas[camada - 1][neuronio]))
                    processamento_da_camada.append(processamento_neuronio)
            
            processamentos_da_rede.append(numpy.array(processamento_da_camada))
            

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
