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

# define o valor do vies da rede neural
bias = 1



