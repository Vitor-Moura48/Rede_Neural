from funcoes_main import *

# loop principal
while True:
    
    # preenche a tela de preto (para ser redesenhada)
    tela.fill((000, 000, 000))

    # função para exibir o fps
    exibir_fps()

    # se todos os players foram eliminados, cria uma nova geração ou partida
    if len(Variaveis_globais.grupo_players) == 0:
        nova_geracao_ou_nova_partida()

    # função para dar update em todos os objetos
    atualizar_objetos()

    # confere o clique para sair
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
            sys.exit()

    # para contralar o jogador no teclado ou joystick
    movimentacao_jogador()

    # define um limite de fps
    Variaveis_globais.clock.tick(fps)

    # atualiza o display
    pygame.display.update() 


   


