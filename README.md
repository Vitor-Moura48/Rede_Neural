# Aprendizado_por_Reforco
Feito por curiosidade sobre redes neurais e por diversão! ⭐


# Descrição do projeto

O objetivo deste projeto é desenvolver um jogo simples no Pygame, onde uma rede neural é utilizada para controlar o jogador e desviar de obstáculos gerados aleatoriamente.


# Arquitetura da Rede Neural

A rede neural utilizada neste jogo possui a seguinte arquitetura:

Camada de Entrada: Composta por 19 neurônios, que representam os inputs do jogo, como a posição do jogador e dos obstáculos.

Camada Oculta: Contém 5 neurônios, responsáveis por processar os dados da camada de entrada e extrair características relevantes para a tomada de decisões do jogador.

Camada de Saída: Composta por 4 neurônios, que controlam os movimentos do jogador, permitindo que ele desvie dos obstáculos de maneira inteligente.

# Funcionamento do algoritimo genético

Para melhorar o desempenho da rede neural, foi empregado o algoritmo genético. A cada geração, são selecionados de dois em dois indivíduos aleatoriamente (com maior chance dos melhores desempenhos) para gerar um novo indivíduo com características semelhantes aos "pais", essa seleção é feita até que a nova população esteja completa. Além disso, existe uma pequena chance de alguns dos genes (pesos) sofrerem mutações durante a criação do novo indivíduo, aumentando a possibilidade de alcançar um melhor desempenho.


# Configurações atuais

Atualmente, o algoritmo utiliza 1500 indivíduos em cada população e enfrenta o desafio de superar 20 obstáculos. Essas configurações foram escolhidas para melhorar o desempenho em um computador padrão.

# Contribuições

Como o projeto ainda está em desenvolvimento, estou aberto a sugestões e melhorias. Se você tiver alguma ideia ou recomendação para aprimorar o jogo ou o algoritmo, sinta-se à vontade para comentar e contribuir!
