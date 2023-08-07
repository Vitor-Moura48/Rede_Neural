from Config import *
import Variaveis_globais as Variaveis_globais


class CriarRedeNeural:
    def __init__(self):

        self.camadas = []

        # lógica para criação mais automatizada da rede neural, variavel de definição rem Config 
        
        for camada in range(len(configuracao_de_camadas) - 1):
            self.camadas.append([])

            for neuronios in range(configuracao_de_camadas[camada + 1]):

                    pesos = numpy.array([0] * configuracao_de_camadas[camada], dtype=float)
                    self.camadas[-1].append(pesos) 


       # se for a primeira geração ele randomiza todos os pesos
        if Variaveis_globais.contador_geracoes == 0:
            self.criar_geracao()
            
        # caso não for a primeira geração, ele faz uma nova a partir da(s) anterior(es)
        else: 
            self.reproduzir_geracao()
        

    def criar_geracao(self):
                
        # randomizando cada peso
        for camada in range(len(self.camadas)):
            for neuronio in range(len(self.camadas[camada])):
                for peso in range(len(self.camadas[camada][neuronio])):
                    self.camadas[camada][neuronio][peso] = round(uniform(-1, 1), 8)
                    self.camadas[camada][neuronio][-1] = bias


    def reproduzir_geracao(self):

        # o melhor individuo sempre será passa do para a próxima geração
        if Variaveis_globais.primeiro_individuo:
            self.camadas = Variaveis_globais.melhor_individuo
            
            Variaveis_globais.primeiro_individuo = False

        # faz um sorteio dos individuos com preferencia dos melhores
        else:

            # função que sorteia os individuos que ainda não foram sorteados
            def roleta():

                roleta = uniform(0, 1)
                primeiro = 0
                ultimo = len(Variaveis_globais.valores_proporcionais) - 1
                meio = (primeiro + ultimo) // 2

                # faz uma busca binaria do individuo sorteado
                while True:

                    if meio == 0 or meio == ultimo or (roleta > Variaveis_globais.valores_proporcionais[meio - 1] and
                        roleta < Variaveis_globais.valores_proporcionais[meio + 1] and Variaveis_globais.ja_sorteados.count(meio) < 2):

                        Variaveis_globais.ja_sorteados.append(meio)
                        break

                    elif roleta > Variaveis_globais.valores_proporcionais[meio]:
                        primeiro = meio + 1
                        meio = (primeiro + ultimo) // 2
                    else:
                        ultimo = meio - 1
                        meio = (primeiro + ultimo) // 2

                return meio
           
            # sorteia dois individuos
            roleta_1 = roleta()
            roleta_2 = roleta()


            # inicia o novo individuo com a mesma estrutura inicial 
            novo_individuo = []

         
            # junta caracteristicas dos dois individuos para formar o novo individuo
            camada_insercao_escolhida = randint(0, len(self.camadas) - 1) 
            neuronio_insercao_escolhida = randint(0, len(self.camadas[camada_insercao_escolhida]) - 1)
            peso_insercao_escolhida = randint(0, len(self.camadas[camada_insercao_escolhida][neuronio_insercao_escolhida]) - 1)



            # une os dois individuos em 1
            for camada in range(len(self.camadas)):
                for neuronio in range(len(self.camadas[camada])):

                    if camada < camada_insercao_escolhida:
                        self.camadas[camada][neuronio] = Variaveis_globais.juncao_de_geracoes[roleta_2][camada][neuronio]
                    
                    elif camada == camada_insercao_escolhida and neuronio < neuronio_insercao_escolhida: 
                        self.camadas[camada][neuronio] = Variaveis_globais.juncao_de_geracoes[roleta_1][camada][neuronio]
                

                    elif camada == camada_insercao_escolhida and neuronio >= neuronio_insercao_escolhida:
                        self.camadas[camada][neuronio] = Variaveis_globais.juncao_de_geracoes[roleta_2][camada][neuronio]
                    
                    elif camada > camada_insercao_escolhida:
                        self.camadas[camada][neuronio] = Variaveis_globais.juncao_de_geracoes[roleta_2][camada][neuronio]
                    
                    else:
                        print('houve alguma exeção!!!!!!')
            


    def randomizar_resultados(self):

        # randomizando cada peso
        for camada in range(len(self.camadas)):
            for neuronio in range(len(self.camadas[camada])):
                for peso in range(len(self.camadas[camada][neuronio]) - 1):
                    if randint(1, 10) == 1:
                        self.camadas[camada][neuronio][peso] = round(uniform(-1, 1))
                    self.camadas[camada][neuronio][peso] = round(uniform(-1, 1), 8)
        
        return (self.camadas)

    
                