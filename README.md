# Rede Neural
Feito por curiosidade sobre redes neurais e por diversão! ⭐


# Descrição do projeto

Este projeto envolve a criação de um jogo interativo usando a biblioteca Pygame, onde uma rede neural é empregada para controlar o jogador e evitar obstáculos gerados aleatoriamente.


# Arquitetura da Rede Neural

O projeto oferece personalização através dos seguintes parâmetros da rede neural:

- Camadas e Neurônios: Você pode ajustar o número de camadas e neurônios em cada camada, permitindo a exploração de diferentes configurações para otimizar o desempenho da rede.

- Indivíduos e Projeteis: A quantidade de indivíduos e projeteis pode ser especificada, permitindo explorar como diferentes tamanhos de populações afetam o processo de aprendizado.

- Partidas por Geração: Cada indivíduo pode jogar múltiplas partidas, reduzindo o impacto do acaso e fornecendo resultados mais confiáveis.

- Camada de Entrada: Você pode escolher o número de projéteis na camada de entrada, ajustando a complexidade da adaptação da rede neural.

- Elitismo: É possível definir quantas cópias do melhor individuo serão feitas, essas cópias são levemente mutadas, visando alguma possível variação vantajosa.

- Recompensa Objetivo: A recompensa objetivo influencia a taxa de mutação dos indivíduos, quanto mais próximo do objetivo, menor a taxa de mutação.

 
# Funcionamento do algoritmo

Para melhorar o desempenho da rede neural, foi empregado o algoritmo genético. A cada geração, são selecionados de dois em dois indivíduos aleatoriamente (com maior chance dos melhores desempenhos) para gerar um novo indivíduo com características semelhantes aos "pais", essa seleção é feita até que a nova população esteja completa. Além disso, existe uma pequena chance de alguns dos genes (pesos) sofrerem mutações durante a criação do novo indivíduo, aumentando a possibilidade de alcançar um melhor desempenho.


# Contribuições

Este projeto está em constante evolução, e qualquer sugestão ou melhoria é bem-vinda. Se você tem ideias para aprimorar o jogo ou o algoritmo, sinta-se à vontade para compartilhar suas recomendações.
