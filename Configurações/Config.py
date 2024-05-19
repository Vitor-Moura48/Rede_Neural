import pygame
from pygame import *

import sys, os, time, copy, math
from functools import cache
from random import *

import json
from cProfile import run

import torch
import torch.nn.functional as F
import numpy


# largura e altura da tela
largura = 800
altura = 800

# inicia o pygame e define um limite de fps
pygame.init()
fps = 9999
clock = pygame.time.Clock()

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

numero_projeteis = 4

  




