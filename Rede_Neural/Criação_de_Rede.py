from Configurações.Config import *
import Configurações.Variaveis_globais as Variaveis_globais


class CriarRedeNeural:  # classe responsável por criar a rede neural
    def __init__(self):

        # variavel onde vão ser colocados os pesos 
        self.camadas = []

        # cria a estrutura com base nas configurações definidas
        for camada in range(1, len(configuracao_de_camadas)):  # 1 porque a primeira camada é  de entrada inicial
            self.camadas.append([])

            for neuronio in range(configuracao_de_camadas[camada]): # +1 porque a primeira camada é apenas a camada de entrada
                # adiciona os pesos (de cada neuronio) na sua respectiva camada
                self.camadas[-1].append(numpy.array([0] * configuracao_de_camadas[camada - 1], dtype=float)) 
        
        # definição da taxa de mutação
        self.taxa_de_mutacao = taxa_de_mutacao_base

        # se for a primeira geração, chama uma função que randomiza todos os pesos
        if Variaveis_globais.contador_geracoes == 0:
            self.iniciar_geracoes()
            
        # caso não for a primeira geração, ele faz uma nova a partir da(s) anterior(es)
        else: 
            self.nova_geracao()

    # função utilizada para criar a primeira geração
    def iniciar_geracoes(self):
                
        # randomizando cada peso de forma aleatória
        for camada in range(len(self.camadas)):
            for neuronio in range(len(self.camadas[camada])):
                for peso in range(len(self.camadas[camada][neuronio])):
                    self.camadas[camada][neuronio][peso] = round(uniform(-1, 1), 16)

    # função utilizada para criar um anova geração
    def nova_geracao(self):

        # o melhor individuo sempre será passado para a próxima geração
        if Variaveis_globais.individuos_elite < numero_de_elitismo:  # pode ser feito mais de uma cópia do melhor indivíduo
          
            # obtem os pesos do melhor indivíduo
            self.camadas = copy.deepcopy(Variaveis_globais.melhor_individuo[1:])
        
            # registra que foi feita mais uma cópia
            Variaveis_globais.individuos_elite += 1

        # faz um sorteio dos individuos com preferencia dos melhores
        else:

            # função que retorna os individuos que podem ser sorteados
            def roleta():

                # variaveis usadas para a roleta
                roleta = uniform(0, 1)
                
                # variaveis usadas para a busca binária
                primeiro = 0
                ultimo = len(Variaveis_globais.valores_proporcionais) - 1
                meio = (primeiro + ultimo) // 2

                # faz uma busca binaria do individuo sorteado
                while True:
                    
                    # se só sobrou uma alternativa ou se a busca encontrou o individuo
                    if meio == primeiro or meio == ultimo or (roleta > Variaveis_globais.valores_proporcionais[meio - 1] and
                        roleta < Variaveis_globais.valores_proporcionais[meio + 1] and Variaveis_globais.ja_sorteados.count(meio) < 4):  # count < indica quantas vezes o mesmo individuo pode ser selecionado

                        # registra o index daquele individuo em uma lista e para a busca
                        Variaveis_globais.ja_sorteados.append(meio)
                        break

                    # se o individuo estiver na metade posterior da metade analizada, elimina a metade anterior (a cada iteração a busca tem mais chances de encontrar)
                    elif roleta > Variaveis_globais.valores_proporcionais[meio]:
                        primeiro = meio + 1
                        meio = (primeiro + ultimo) // 2
                    
                    # mesma lógica, elimina a metade posterior (em vez da anterior)
                    else:
                        ultimo = meio - 1
                        meio = (primeiro + ultimo) // 2

                # retorna o index do individuo sorteado
                return meio
           
            # sorteia dois individuos
            roleta_1 = roleta()
            roleta_2 = roleta()

            # calcula a média do desempenho dos dois individuos sorteados
            media_de_recompensa = ((Variaveis_globais.juncao_de_geracoes[roleta_1][0][0] + Variaveis_globais.juncao_de_geracoes[roleta_2][0][0]) / 2) 

            # reduz um pouco a taxa de mutação base de acordo com a aproximação do objetivo
            self.taxa_de_mutacao = taxa_de_mutacao_base - (media_de_recompensa / recompensa_objetivo)

            # junta caracteristicas dos dois individuos para formar o novo individuo, sorteando o ponto que vai ser unido
            camada_insercao_escolhida = randint(0, len(self.camadas) - 1) 
            neuronio_insercao_escolhida = randint(0, len(self.camadas[camada_insercao_escolhida]) - 1)

            # combina os dois individuos
            for camada in range(len(self.camadas)):
                for neuronio in range(len(self.camadas[camada])):

                    if camada < camada_insercao_escolhida or (camada == camada_insercao_escolhida and neuronio < neuronio_insercao_escolhida):                                         
                        self.camadas[camada][neuronio] = Variaveis_globais.juncao_de_geracoes[roleta_1][camada + 1][neuronio]# camada +1 porque a primeira camada = fitness
                  
                    elif camada > camada_insercao_escolhida or (camada == camada_insercao_escolhida and neuronio >= neuronio_insercao_escolhida):
                        self.camadas[camada][neuronio] = Variaveis_globais.juncao_de_geracoes[roleta_2][camada + 1][neuronio]
                 
    # função utilizada para simular a mutação
    def randomizar_resultados(self):

        # randomizando cada peso de acordo com a taxa de mutação
        for camada in range(len(self.camadas)):
            for neuronio in range(len(self.camadas[camada])):
                for peso in range(len(self.camadas[camada][neuronio])):
        
                    # quanto maior a taxa de mutação, mais provavel é a alteração
                    if uniform(0, 1) <= self.taxa_de_mutacao:
                        self.camadas[camada][neuronio][peso] = round(uniform(-1, 1), 16) 

        # retorna todos os pesos do individuo deposi da mutação
        return (self.camadas)

    
                