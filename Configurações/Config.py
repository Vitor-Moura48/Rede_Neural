import pygame
from pygame import *

import sys, os, time, copy
from functools import cache
from random import *

import json
from cProfile import run

import torch
import torch.nn.functional as F
import numpy

# largura e altura da tela
largura = 1500
altura = 500

# inicia o pygame e define um limite de fps
pygame.init()
fps = 9999

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

# seleciona alguma pré configuração, para testes
arquivo = 2

# teste padrão
if arquivo == 0:
    pass

elif arquivo == 1:
   pass

elif arquivo == 2:

    # define o número de player (até dois)
    quantidade_jogadores = 0
    
    bias = 1

    convolucional = False
    if convolucional:
        alcance_de_visao = 160
        quantidade_sensores_x = (alcance_de_visao // dimensoes_projetil[0])
        quantidade_sensores_y = (alcance_de_visao // dimensoes_projetil[1])
        quantidade_entradas = quantidade_sensores_x * quantidade_sensores_y + 2
    else:
        projeteis_para_entrada = 1
        quantidade_entradas = (projeteis_para_entrada * 4) + 2
   
        
    configuracao_de_camadas = (quantidade_entradas, quantidade_entradas * 2, 4, 4)
    funcoes_de_camadas = (2, 2, 2, True)

    # quantas partidas vão ter por geração (quanto mais partidas, mais confiavel o resultado, porém, mais lento)
    partidas_por_geracao = 30

    numero_projeteis = 4
    numero_players = 800

    numero_de_elitismo = numero_players * 0.5

    taxa_de_mutacao_base = 0.05
    # definição da taxa de mutação (para o elitismo)
    taxa_de_mutacao_elite = 0.01
  
    recompensa_objetivo = 10000 * (1 / taxa_de_mutacao_base)





