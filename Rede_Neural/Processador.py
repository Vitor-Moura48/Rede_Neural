from Configurações.Config import *
import Configurações.Variaveis_globais as Variaveis_globais


# classe que gerencia o player
class Processador:
    def __init__(self, indice, *args):

        # indice que o player vai ser colocado na variavel geração atual
        self.indice = indice
    
        # variavel que vai armazenar todos os pesos daquela rede (gerados na criação de rede)
        self.camadas = []

        # cada arg é uma camada
        for arg in args:
            self.camadas.append(arg)
        
    # funções de ativação (usadas no final)
    def funcao_sigmoide(self, entrada):
        saida = 1 / (1 + numpy.exp(-entrada))
        return saida

    def funcao_relu(self, entrada):
        if entrada < 0:
            entrada = 0
        return entrada

    # função para retornar as entradas para a rede neural
    def obter_entradas(self):

        # variavel que vai ser retornada após passar pelas funções
        resultados_sensores = []

        # função que obtem as distâncias de cada inimigo para o jogador e retorna o valor
        def obter_distancias():
            for projetil in Variaveis_globais.grupo_projeteis:

                informacoes_inimigo = projetil.informar_posicao()
                distancia_x = 1 - (abs(informacoes_inimigo[0] - Variaveis_globais.grupo_players[Variaveis_globais.grupo_processadores.index(self)].rect_player.center[0]) / 110)
                distancia_y = 1 - (abs(informacoes_inimigo[1] - Variaveis_globais.grupo_players[Variaveis_globais.grupo_processadores.index(self)].rect_player.center[1]) / 110)
            
                distancia = (distancia_x ** 2 + distancia_y ** 2) ** 0.5

                # retorna junto algumas outras informações
                resultados_sensores.append([distancia, distancia_x, distancia_y, informacoes_inimigo[2], informacoes_inimigo[3], velocidade_projetil])

        # função que ordena cada coordenada (dos inimigos) de acordo com os que estão mais próximos
        def ordenar_cada_inimigo():
            resultados_sensores.sort(key=lambda x: x[0])

        # função que apaga as coordenadas exedentes e apaga a distancia absoluta dos resultados (usada para "ordenar cada inimigo")
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
    
    # atualiza o estado da rede a cada iteração
    def update(self):
       
        # obtem as informações dos projeteis mais próximos
        resultados = self.obter_entradas()

        # variavel que vai conter os dados de entrada da rede
        entrada_da_rede = []

        # adiciona como entrada a distancia para cada canto da tela
        entrada_da_rede.append((Variaveis_globais.grupo_players[Variaveis_globais.grupo_processadores.index(self)].rect_player.center[0] / 750) -1)
        entrada_da_rede.append((Variaveis_globais.grupo_players[Variaveis_globais.grupo_processadores.index(self)].rect_player.center[1] / 250) -1)
        
        # junta todos os dados que vão para a entrada da rede em uma única lista
        for coordenada in resultados:
            for valor in coordenada:
                entrada_da_rede.append(valor)

        # transforma as listas em arrays (para facilitar os calculos)
        entradas_1 = numpy.array(entrada_da_rede)

        # armazena o resultado dos calculos de cada neuronios e divide em camadas
        processamentos_da_rede = []

        # Faz todos os calculos de cada camada e armazena na variavel acima
        for camada in range(1, len(configuracao_de_camadas)):

            # zera o processamento da camada a cada iteração do for
            processamento_da_camada = []

            # se for a primeira camada, faz os calculos com a lista de entradas já obtida
            if camada == 1:

                # multiplica cada valor de entrada pelo seu respectivo peso, soma tudo e passa esse valor pelafunção de ativação (para cada neuronio de cada camada)
                for neuronio in range(configuracao_de_camadas[camada]):       
                    processamento_neuronio = self.funcao_relu(sum(entradas_1 * self.camadas[camada - 1][neuronio]))

                    # adiciona o processamento do neuronio na lista daquela camada
                    processamento_da_camada.append(processamento_neuronio)             
                
            else:
                # mesma lógica, porém usa a camada anterior como entrada para a camada atual
                for neuronio in range(configuracao_de_camadas[camada]):          
                    processamento_neuronio = self.funcao_relu(sum(processamentos_da_rede[-1] * self.camadas[camada - 1][neuronio]))
                    processamento_da_camada.append(processamento_neuronio)
            
            # a cada camada concluída, adiciona ela em uma lista (para ser usada como entrada para a próxima)
            processamentos_da_rede.append(numpy.array(processamento_da_camada))
        
        # variavel que contem o valor de saída da rede neural
        self.comandos = processamentos_da_rede[-1]
            
