import pygame
from pygame import *
import sys
import numpy
from random import *
import math
import time
import copy
import os
import json
from cProfile import run
import torch

# largura e altura da tela
largura = 1500
altura = 500

# inicia o pygame e define um limite de fps
pygame.init()
fps = 999

velocidade_projetil = 8  # 10 max no caso
velocidade_ia = 10  # 9 max no caso (10 inimogo, 10 player) 10 + 9 = 19  -- 20 (10 + 10)

# define dimensões e cor da tela
tela = pygame.display.set_mode((largura, altura))
tela.fill((000, 000, 000))

dimensoes_projetil = (10, 10)
dimensoes_rede = (10, 10)

# difine a fonte e um texto inicial para a tela
fonte = pygame.font.Font(None, 32)
mensagem_fps_para_tela = fonte.render('fps 0', True, (255, 000, 000))

# define o número de player (até dois)
quantidade_jogadores = 0

# quantas partidas vão ter por geração (quanto mais partidas, mais confiavel o resultado, porém, mais lento)
partidas_por_geracao = 10

convolucional = False

# seleciona alguma pré configuração, para testes
arquivo = 2

# teste padrão
if arquivo == 0:
    # define o valor do vies da rede neural
    bias = 1

    # quantos projeteis vão ser passados para a rede (se 5, os 5 mais próximos vão ser passados)
    projeteis_para_entrada = 8

    # variavel que armazena o valor total de entradas a partir de quantos projeteis vão ser colocados
    quantidade_entradas = (projeteis_para_entrada * 5) + 2

    # define quantas camadas vão ter e quantos neuronios em cada uma
    configuracao_de_camadas = (quantidade_entradas, 9, 4)

    # define o número de players e inimigos
    numero_projeteis = 15
    numero_players = 200

    # porcentagem de players que vão ser feitas a partir do melhor individuo
    numero_de_elitismo = numero_players * 0.2

    # chance de mutação de um peso ao passar pela fução de mutação
    taxa_de_mutacao_base = 0.1

    # faz a conta considerando a taxa de mutação base (o valor a esquerda é o necessario para chegar a 0 de taxa de mutação)
    recompensa_objetivo = 10000 * (1 / taxa_de_mutacao_base)

### abaixo são os outros testes, fazem a mesma coisa que o primeiro

elif arquivo == 1:
    # define o valor do vies da rede neural
    bias = 0

    projeteis_para_entrada = 4

    quantidade_entradas = (projeteis_para_entrada * 5) + 2

    configuracao_de_camadas = (quantidade_entradas, quantidade_entradas, 4)

    numero_projeteis = 15
    numero_players = 1500

    numero_de_elitismo = numero_players * 0.4

    taxa_de_mutacao_base = 0.1

    recompensa_objetivo = 10000 * (1 / taxa_de_mutacao_base)

# teste com entradas minimas, elitismo médio
elif arquivo == 2:

    bias = 0

    if convolucional:
        alcance_de_visao = 160
        quantidade_sensores_x = (alcance_de_visao // dimensoes_projetil[0])
        quantidade_sensores_y = (alcance_de_visao // dimensoes_projetil[1])
        quantidade_entradas = quantidade_sensores_x * quantidade_sensores_y + 2
    else:
        projeteis_para_entrada = 1
        quantidade_entradas = (projeteis_para_entrada * 4) + 2
   
        
    configuracao_de_camadas = (quantidade_entradas, quantidade_entradas * 2, 4)
    funcoes_de_camadas = (2, 2, False)

    numero_projeteis = 4
    numero_players = 200

    numero_de_elitismo = numero_players * 0.5

    taxa_de_mutacao_base = 0.05
  
    recompensa_objetivo = 4000 * (1 / taxa_de_mutacao_base)





