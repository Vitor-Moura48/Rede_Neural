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
fps = 120

velocidade_projetil = 6  # 10 max no caso
velocidade_ia = 6  # 9 max no caso (10 inimogo, 10 player) 10 + 9 = 19  -- 20 (10 + 10)

tela = pygame.display.set_mode((largura, altura))
tela.fill((000, 000, 000))


fonte = pygame.font.Font(None, 32)
mensagem_fps_para_tela = fonte.render('fps 0', True, (255, 000, 000))

arquivo = 0

if arquivo == 0:
    # define o valor do vies da rede neural
    bias = 1
    projeteis_para_entrada = 8

    quantidade_entradas = (projeteis_para_entrada * 3) + 2

    configuracao_de_camadas = (quantidade_entradas, 5, 4)

    numero_inimigos = 20
    numero_players = 1500

    numero_de_elitismo = numero_players * 0.1

    taxa_de_mutacao_base = 0.1

    recompensa_objetivo = 100000


elif arquivo == 1:
    # define o valor do vies da rede neural
    bias = 1

    projeteis_para_entrada = 4

    quantidade_entradas = (projeteis_para_entrada * 3) + 2

    configuracao_de_camadas = (quantidade_entradas, 5, 4)

    numero_inimigos = 20
    numero_players = 1500

    numero_de_elitismo = numero_players * 0.1

    taxa_de_mutacao_base = 1

    recompensa_objetivo = 3000

elif arquivo == 2:
    # define o valor do vies da rede neural
    bias = 1

    projeteis_para_entrada = 1

    quantidade_entradas = (projeteis_para_entrada * 3) + 2

    configuracao_de_camadas = (quantidade_entradas, 10, 4)

    numero_inimigos = 20
    numero_players = 1500

    numero_de_elitismo = numero_players * 0.1

    taxa_de_mutacao_base = 1

    recompensa_objetivo = 4000




