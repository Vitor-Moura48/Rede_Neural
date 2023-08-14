import pygame
from pygame import *
import sys
import numpy
from random import *
import math
import time
import copy


# largura e altura da tela
largura = 1500
altura = 500

# inicia o pygame e define um limite de fps
pygame.init()
fps = 240

velocidade_projetil = 6  # 10 max no caso
velocidade_ia = 6  # 9 max no caso (10 inimogo, 10 player) 10 + 9 = 19  -- 20 (10 + 10)

tela = pygame.display.set_mode((largura, altura))
tela.fill((000, 000, 000))


fonte = pygame.font.Font(None, 32)
mensagem_fps_para_tela = fonte.render('fps 0', True, (255, 000, 000))

partidas_por_geracao = 10

arquivo = 2

# teste padrão
if arquivo == 0:
    # define o valor do vies da rede neural
    bias = 1
    projeteis_para_entrada = 8

    quantidade_entradas = (projeteis_para_entrada * 5) + 4

    configuracao_de_camadas = (quantidade_entradas, 9, 4)

    numero_inimigos = 15
    numero_players = 200

    numero_de_elitismo = numero_players * 0.2

    taxa_de_mutacao_base = 0.1

    recompensa_objetivo = 100000

# teste padrão modificado
elif arquivo == 1:
    # define o valor do vies da rede neural
    bias = 0

    projeteis_para_entrada = 4

    quantidade_entradas = (projeteis_para_entrada * 5) + 4

    configuracao_de_camadas = (quantidade_entradas, quantidade_entradas, 4)

    numero_inimigos = 15
    numero_players = 1500

    numero_de_elitismo = numero_players * 0.4

    taxa_de_mutacao_base = 0.1

    recompensa_objetivo = 100000

# teste com entradas minimas, elitismo médio, objetivo: 5000 loops
elif arquivo == 2:

    bias = 0

    projeteis_para_entrada = 1

    quantidade_entradas = (projeteis_para_entrada * 5) + 4

    configuracao_de_camadas = (quantidade_entradas, 9, 4)

    numero_inimigos = 15
    numero_players = 600

    numero_de_elitismo = numero_players * 0.5

    taxa_de_mutacao_base = 0.1

    recompensa_objetivo = 50000




