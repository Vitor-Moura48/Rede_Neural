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

# ajuda a selecionar o melhor individuo de cada geração
melhor_tempo = 0

contador_geracoes = 0

geracao_avo = []
geracao_anterior = []
geracao_atual = []

juncao_de_geracoes = []
valores_proporcionais = []

ja_sorteados = []


# variavel para ajudar a manter sempre o melhor player
primeiro_individuo = True

# variavel para ajudar a direcionar os primeiros projeteis exatamente na direção do surgimento do player, para eliminar os piores
primeiro_inimigo = 0
