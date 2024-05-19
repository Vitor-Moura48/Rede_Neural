from Configurações.Config import *
import Configurações.Global as Global
from Rede_Neural.rede_neural import RedeNeural

class Player:
    def __init__(self, real=False):

        self.rede_neural = RedeNeural([6, 12, 6, 4], ['leaky_relu', 'leaky_relu', 'leaky_relu'], 0, 0.06)

        # define se o player é ou não um jogador
        self.real = real

        # variavel para contar a quantidade de loops que o player conseguiu passar
        self.tick = 0

        # define o ponto de spaw do player
        self.posicao_x = largura / 2
        self.posicao_y = altura / 2

        self.valor_de_ativacao = self.valor_de_ativacao()

        # cria um retandulo de colisão e mostra na tela
        self.rect = pygame.Rect((self.posicao_x, self.posicao_y, dimensoes_rede[0], dimensoes_rede[1]))
     
    # retorna o valor mínimo para ativar o neuronio
    def valor_de_ativacao(self):
        
        # se for sigmoid, o valor mínimo é 0.5
        if funcoes_de_camadas[-2] == 1:
            return 0.5
        
        # se for Relu, o valor mínimo é 0
        elif funcoes_de_camadas[-2] == 2:
            return 0
        
        # se for Tangente Hiperbólica, o valor mínimo é 0
        elif funcoes_de_camadas[-2] == 3:
            return 0
    
    # função para retornar as entradas para a rede neural
    def obter_entradas(self):

        # variavel que vai ser retornada após passar pelas funções
        resultados_sensores = []

        if convolucional:
            contador_sesores_da_linha = 0
             
            ponto_inicial = [self.rect.left - ((alcance_de_visao - self.rect.width) // 2), 
                             self.rect.top - ((alcance_de_visao - self.rect.height) // 2)]
            
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
                for projetil in Global.grupo_projeteis.values():
                    
                    informacoes_inimigo = projetil.informar_posicao()

                    # calcul o quão distnte o projetil está do player (1 = o projetil mais distante à direita, -1 à esquerda)
                    distancia_x = (informacoes_inimigo[0] - self.rect.center[0]) / largura
                    distancia_y = (informacoes_inimigo[1] - self.rect.center[1]) / altura
                  
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
        
        entradas = [(self.rect.center[0] / (largura / 2)) -1, (self.rect.center[1] / (altura / 2)) -1]

        for projetil in resultados_sensores:
            entradas.extend(projetil)
            

        # retorna as coordenadas mais próximas
        return entradas
    
    # atualiza o estado do player a cada geração
    def update(self):
       
        # se não for um jogador, conta os loops e se movimenta a partir dos comandos da sua rede
        if self.real == False:

            # conta os loops
            self.tick += 1

            self.rede_neural.definir_entrada(self.obter_entradas())
            output = self.rede_neural.obter_saida()

            if output[0]:
                self.posicao_x += velocidade_ia
                                
            if output[1]:
                self.posicao_x -= velocidade_ia
                                    
            if output[2]:
                self.posicao_y += velocidade_ia             

            if output[3]:
                self.posicao_y -= velocidade_ia
                
                    
            # cria um retandulo de colisão e mostra na tela
            self.rect.center = (self.posicao_x, self.posicao_y)
            draw.rect(tela, (000, 000, 255), self.rect)
            draw.rect(tela, (000, 255, 000), self.rect, 2)

        # se for um jogador troca a cor do player
        else:          
    
            # cria um retandulo de colisão e mostra na tela
            self.rect.center = (self.posicao_x, self.posicao_y)
            draw.rect(tela, (000, 255, 000), (self.posicao_x - 5, self.posicao_y - 5, dimensoes_rede[0], dimensoes_rede[1]))