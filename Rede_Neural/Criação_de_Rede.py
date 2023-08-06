from Jogo.Config import *
import Jogo.Variaveis_globais as Variaveis_globais


class CriarRedeNeural:
    def __init__(self):

       # se for a primeira geração ele cria os pesos e randomiza-os
        if Variaveis_globais.contador_geracoes == 0:
            self.resultado = self.criar_geracao()
            
        # caso não for a primeira geração, ele faz uma nova a partir da(s) anterior(es)
        else: 
            self.resultado = self.reproduzir_geracao()
        

    def criar_geracao(self):

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
                self.grupo_neuronios_primeira_camada_oculta[neuronio][peso] = round(uniform(-1, 1), 8)
            self.grupo_neuronios_primeira_camada_oculta[neuronio][-1] = bias

        for neuronio in range(len(self.grupo_neuronios_camada_de_saida)):
            for peso in range(5):
                self.grupo_neuronios_camada_de_saida[neuronio][peso] = round(uniform(-1, 1), 8)
            self.grupo_neuronios_camada_de_saida[neuronio][-1] = bias
        
        return (self.grupo_neuronios_primeira_camada_oculta, self.grupo_neuronios_camada_de_saida)
    

    
    def reproduzir_geracao(self):

        # o melhor individuo sempre será passa do para a próxima geração
        if Variaveis_globais.primeiro_individuo:
            self.grupo_neuronios_primeira_camada_oculta = copy.deepcopy(Variaveis_globais.melhor_peso_primeira_camada_oculta)
            self.grupo_neuronios_camada_de_saida = copy.deepcopy(Variaveis_globais.melhor_peso_camada_de_saida)

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

            novo_individuo = [[], []]

            # junta caracteristicas dos dois individuos para formar o novo individuo
            camada = randint(1, 2)

            if camada == 1:

                neuronio = randint(0, 18)


                novo_individuo[0] = Variaveis_globais.juncao_de_geracoes[roleta_1][1][:neuronio + 1]
                if neuronio != 18:
                    novo_individuo[0] += Variaveis_globais.juncao_de_geracoes[roleta_2][1][neuronio + 1:]


                novo_individuo[1] = Variaveis_globais.juncao_de_geracoes[roleta_2][2]

            elif camada == 2:
                neuronio = randint(0, 4)

                novo_individuo[0] = Variaveis_globais.juncao_de_geracoes[roleta_1][1]

                novo_individuo[1] = Variaveis_globais.juncao_de_geracoes[roleta_1][2][:neuronio + 1]
                if neuronio != 4:
                    novo_individuo[1] += Variaveis_globais.juncao_de_geracoes[roleta_2][2][neuronio + 1:]

    
            # adiciona cada conjunto de pesos nas variaveis
            self.grupo_neuronios_primeira_camada_oculta = novo_individuo[0]
            self.grupo_neuronios_camada_de_saida = novo_individuo[1]
           

    def randomizar_resultados(self):

        # percorre cada neuronio e cada peso do neuronio e randomiza-os
        for neuronio in range(len(self.grupo_neuronios_primeira_camada_oculta)):

            for peso in range(len(self.grupo_neuronios_primeira_camada_oculta[neuronio]) - 1):
                if randint(1, 10) == 1:
                    self.grupo_neuronios_primeira_camada_oculta[neuronio][peso] = round(uniform(-1, 1), 8)

        for neuronio in range(len(self.grupo_neuronios_camada_de_saida)):

            for peso in range(len(self.grupo_neuronios_camada_de_saida[neuronio]) - 1):
                if randint(1, 10) == 1:
                    self.grupo_neuronios_camada_de_saida[neuronio][peso] = round(uniform(-1, 1), 8)
        
        return (self.grupo_neuronios_primeira_camada_oculta, self.grupo_neuronios_camada_de_saida)

    
                