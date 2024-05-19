from Configurações.Config import *
from Rede_Neural import estrategia_evolutiva
from . import player, projeteis

#classe para conferir conliões
class Colisoes:

    # função para conferir as colisões com o player
    def condicoes_exclusao(self, objeto):
        if objeto.rect.collidelist([projetil.rect for projetil in projeteis.grupo_projeteis]) != -1:
            estrategia_evolutiva.gerenciador.desativar_agente(objeto)
            objeto.spaw()
        
        elif objeto.rect.bottom < 0 or objeto.rect.top > altura or objeto.rect.left < 0 or objeto.rect.right > largura:
            estrategia_evolutiva.gerenciador.desativar_agente(objeto)
            objeto.spaw()
    
    # função para chamar as funções de colisão a cada iteração
    def update(self):
        for agente in estrategia_evolutiva.gerenciador.agentes[:]:
            self.condicoes_exclusao(agente)
        
        try: 
            if player.jogador.rect.collidelist([projetil.rect for projetil in projeteis.grupo_projeteis]) != -1:
                player.jogador = None
        except: pass



