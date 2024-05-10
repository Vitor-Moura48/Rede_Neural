from Configurações.Config import *
import Configurações.Variaveis_globais as Variaveis_globais

# classe que gerencia o player
class Processador:
    def __init__(self, indice, camadas):

        self.indice = indice
        self.camadas = camadas
    
        # variavel que vai armazenar todos os pesos daquela rede (gerados na criação de rede)
        self.tensores = [torch.tensor(camada, dtype=torch.float64) for camada in camadas] ##############################

    # seleciona a função de ativação de acordo com a configuração
    def aplicar_ativacao(self, tensor, tipo):

        if tipo == 1:
            return F.sigmoid(tensor)
            
        elif tipo == 2:
            return F.relu(tensor)
        
        elif tipo == 3:
            return F.tanh(tensor)
    
        if tipo == 4:
            return F.leaky_relu(tensor)

    # função para retornar as entradas para a rede neural
    def obter_entradas(self):

        # variavel que vai ser retornada após passar pelas funções
        resultados_sensores = []

        if convolucional:
            contador_sesores_da_linha = 0
             
            ponto_inicial = [Variaveis_globais.grupo_players[self.indice].rect.left - ((alcance_de_visao - Variaveis_globais.grupo_players[self.indice].rect.width) // 2), 
                             Variaveis_globais.grupo_players[self.indice].rect.top - ((alcance_de_visao - Variaveis_globais.grupo_players[self.indice].rect.height) // 2)]
            
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
                for projetil in Variaveis_globais.grupo_projeteis.values():
                    
                    informacoes_inimigo = projetil.informar_posicao()

                    # calcul o quão distnte o projetil está do player (1 = o projetil mais distante à direita, -1 à esquerda)
                    distancia_x = (informacoes_inimigo[0] - Variaveis_globais.grupo_players[self.indice].rect.center[0]) / largura
                    distancia_y = (informacoes_inimigo[1] - Variaveis_globais.grupo_players[self.indice].rect.center[1]) / altura
                  
                    distancia = math.hypot(distancia_x, distancia_y)

                    # retorna junto algumas outras informações
                    resultados_sensores.append([distancia, distancia_x, distancia_y, informacoes_inimigo[2], informacoes_inimigo[3]])

            # função que ordena cada coordenada (dos inimigos) de acordo com os que estão mais próximos
            def ordenar_distancias():
                resultados_sensores.sort(key=lambda x: x[0])

            # função que apaga as coordenadas exedentes e apaga a distancia absoluta dos resultados (usada para "ordenar cada inimigo")
            def normatizar_o_resultado():
                while len(resultados_sensores) > projeteis_para_entrada:
                    resultados_sensores.pop(-1)
            
                for coordenada in range(projeteis_para_entrada):  
                    resultados_sensores[coordenada].pop(0)

            # chama todas essas funções
            obter_distancias()
            ordenar_distancias()
            normatizar_o_resultado()
            

        # retorna as coordenadas mais próximas
        return resultados_sensores

    # atualiza o estado da rede a cada iteração
    def update(self):
    
        # obtem as informações dos projeteis mais próximos
        resultados = self.obter_entradas()
        
        # variavel que vai conter os dados de entrada da rede
        entrada_da_rede = [(Variaveis_globais.grupo_players[self.indice].rect.center[0] / (largura / 2)) -1, (Variaveis_globais.grupo_players[self.indice].rect.center[1] / (altura / 2)) -1]

        if convolucional:
            for sensor in resultados:
                entrada_da_rede.append(sensor)
        
        else:
            # junta todos os dados que vão para a entrada da rede em uma única lista
            for projetil in resultados:
                entrada_da_rede.extend(projetil)
        
        # armazena o resultado das entradas ou de alguma fase intermediária
        self.estado_atual_da_rede = torch.tensor(entrada_da_rede, dtype=torch.float64)  ###########################################

        # Faz todos os calculos de cada camada e armazena na variavel acima
        for camada in range(1, len(configuracao_de_camadas)):

            saida_camada_tensor = torch.matmul(self.estado_atual_da_rede, self.tensores[camada - 1].t()) + bias ###########################################
            saida_camada_tensor_ativada = self.aplicar_ativacao(saida_camada_tensor, Variaveis_globais.funcoes_de_camadas[camada - 1])
            self.estado_atual_da_rede = saida_camada_tensor_ativada ######################################

        if funcoes_de_camadas[-1] == True:
            self.estado_atual_da_rede = torch.softmax(self.estado_atual_da_rede, dim=0) ########################################

        # variavel que contem o valor de saída da rede neural
        self.comandos = self.estado_atual_da_rede.tolist()
