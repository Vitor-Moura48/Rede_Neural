from funcoes_main import Global, pygame, QUIT, sys, MOUSEBUTTONDOWN, K_ESCAPE, display
import funcoes_main

class Tela():
    def __init__(self, botoes=[], icones=[], textos=[], esq=None, fill=True): # componente = objeto,função

        self.selecionou = False
        self.botoes = botoes
        self.icones = icones
        self.textos = textos
        self.esq = esq
        
        for componente in Global.componentes:
            componente.kill()
        
        self.textos = [texto for texto in self.textos]

        for icone in self.icones:
            Global.componentes.add(icone)
    
        for botao in self.botoes:
            Global.componentes.add(botao[0])
            Global.componente_botao.add(botao[0])

        Global.tela.fill((000, 000, 000)) if fill else None

    def loop(self):
        self.posicao_mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
                sys.exit()
            
            if event.type == pygame.VIDEORESIZE:
                    funcoes_main.ajustar_tela()
                    for componente in Global.componentes:
                        componente.ajustar_posicoes()
                    ajustar = [texto.ajustar_posicoes() for texto in self.textos]

            if self.botoes:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    for botao in self.botoes:
                        if botao[0].rect.collidepoint(self.posicao_mouse):
                            botao[1]()
                            self.selecionou = True if botao[2] == True else None
            
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.selecionou = True
                    self.esq() if self.esq != None else None 

    def atualizar(self):
        Global.componentes.draw(Global.tela)
        Global.componentes.update()
        update = [texto.update() for texto in self.textos]
        display.flip()
        