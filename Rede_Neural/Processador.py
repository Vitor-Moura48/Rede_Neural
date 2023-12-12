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
    def sigmoid(self, entrada):
        saida = 1 / (1 + numpy.exp(-entrada))
        return saida

    def relu(self, entrada):
        return numpy.maximum(0, entrada)

    def tangente_hiperbolica(self, entrada):
        saida = (numpy.e ** entrada - numpy.e ** -entrada) / (numpy.e ** entrada + numpy.e ** -entrada)
        return saida

    # utilizada para obter a porcentagem de cada 'saida final' de acordo com a proporção
    def funcao_softmax(self, saidas):
        resultado = numpy.exp(saidas)/sum(numpy.exp(saidas))
        
        return resultado
   
    # seleciona a função de ativação de acordo com a configuração
    def selecionar_ativacao(self, entradas, camada, neuronio, tipo):
        
        if tipo == 1:
            return self.sigmoid(sum(entradas * self.camadas[camada - 1][neuronio]))

        elif tipo == 2:
            return self.relu(sum(entradas * self.camadas[camada - 1][neuronio]))
        
        elif tipo == 3:
            return self.tangente_hiperbolica(sum(entradas * self.camadas[camada - 1][neuronio]))


    # função para retornar as entradas para a rede neural
    def obter_entradas(self):

        # variavel que vai ser retornada após passar pelas funções
        resultados_sensores = []

        if convolucional:
            contador_sesores_da_linha = 0
             

            ponto_inicial = [Variaveis_globais.grupo_players[Variaveis_globais.grupo_processadores.index(self)].rect_player.left - ((alcance_de_visao - Variaveis_globais.grupo_players[Variaveis_globais.grupo_processadores.index(self)].rect_player.width) // 2), 
                             Variaveis_globais.grupo_players[Variaveis_globais.grupo_processadores.index(self)].rect_player.top - ((alcance_de_visao - Variaveis_globais.grupo_players[Variaveis_globais.grupo_processadores.index(self)].rect_player.height) // 2)]
            
            
            for i in range(quantidade_entradas - 2): 
                contador_sesores_da_linha += 1

                if ponto_inicial[0] <= 0:
                    ponto_inicial[0] = 1
                if ponto_inicial[0] >= largura:
                    ponto_inicial[0] = largura - 1 
                if ponto_inicial[1] <= 0:
                    ponto_inicial[1] = 1
                if ponto_inicial[1] >= altura:
                    ponto_inicial[1] = altura - 1  

            
                if tela.get_at(ponto_inicial)[0] == 0:
                    resultados_sensores.append(0)
                elif tela.get_at(ponto_inicial)[0] == 255:
                    resultados_sensores.append(1)
                else:
                    resultados_sensores.append(0.5)
                
                if contador_sesores_da_linha < (quantidade_sensores_x):
                    ponto_inicial[0] += dimensoes_projetil[0]
                else:
                    ponto_inicial[0] -= (dimensoes_projetil[0] * (quantidade_sensores_x - 1))
                    ponto_inicial[1] += dimensoes_projetil[1]

                    contador_sesores_da_linha = 0

        
        else:
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
        

        if convolucional:
            for sensor in resultados:
                entrada_da_rede.append(sensor)
        
        else:
            # junta todos os dados que vão para a entrada da rede em uma única lista
            for coordenada in resultados:
                for valor in coordenada:
                    entrada_da_rede.append(valor)

        # transforma as listas em arrays (para facilitar os calculos)
        self.entradas_1 = numpy.array(entrada_da_rede)

        # armazena o resultado dos calculos de cada neuronios e divide em camadas
        self.processamentos_da_rede = []

        # Faz todos os calculos de cada camada e armazena na variavel acima
        for camada in range(1, len(configuracao_de_camadas)):

            # zera o processamento da camada a cada iteração do for
            processamento_da_camada = []
            

            # se for a primeira camada, faz os calculos com a lista de entradas já obtida
            if camada == 1:
                
                # multiplica cada valor de entrada pelo seu respectivo peso, soma tudo e passa esse valor pelafunção de ativação (para cada neuronio de cada camada)
                for neuronio in range(configuracao_de_camadas[camada]):       
                    processamento_neuronio = self.selecionar_ativacao(self.entradas_1, camada, neuronio, funcoes_de_camadas[camada - 1])

                    # adiciona o processamento do neuronio na lista daquela camada
                    processamento_da_camada.append(processamento_neuronio)             
                
            else:
                # mesma lógica, porém usa a camada anterior como entrada para a camada atual
                for neuronio in range(configuracao_de_camadas[camada]):     
                    processamento_neuronio = self.selecionar_ativacao(self.processamentos_da_rede[-1], camada, neuronio, funcoes_de_camadas[camada - 1])
                    processamento_da_camada.append(processamento_neuronio)
            
            # a cada camada concluída, adiciona ela em uma lista (para ser usada como entrada para a próxima)
            self.processamentos_da_rede.append(numpy.array(processamento_da_camada))
        
        if funcoes_de_camadas[-1] == True:
            self.processamentos_da_rede[-1] = self.funcao_softmax(self.processamentos_da_rede[-1])
        
        # variavel que contem o valor de saída da rede neural
        self.comandos = self.processamentos_da_rede[-1]
            
