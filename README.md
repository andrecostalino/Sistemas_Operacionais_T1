# Trabalho Sistemas Microprocessados
Esse trabalho consiste em um jogo no qual ocorre condições de corrida que são solucionadas de formas variadas.
##O Jogo
Ele consiste numa competição entre dois cozinheiros que trabalham em um restaurante. Ambos tem como objetivo completar o máximo de pratos possível dentre os que estão presentes no cardápio do restaurante. Os cozinheiros dividem a mesma dispensa, e essa não pode ser acessada por ambos simultaneamente, logo parte da competição é a utilização eficiente do tempo e ingredientes a disposição para atingir o objetivo de três pontos antes do oponenete, vencendo o jogo.
###Cardapio
- Burrito: Feijão, Queijo e Carne
- Hámburguer: Pão, Queijo e Carne
- Salada: Alface, Tomate e Queijo
##Condições de Corrida
O jogo possui duas regiões críticas nas quais podem ocorrer condições de corrida, a dispensa compartilhada e a lista com as pontuações dos jogadores. Esses espaços não podem ser acessados simultaneamente, para que não ocorra nenhuma coleta ou escrita de dados equivocados nelas. As condições de corrida foram solucionadas de três formas diferentes: 
1.Lock
2.Semáforo
3.Monitor
###Lock
A solução por lock consite na criação de dois locks no princípio do jogo, o lock dos ingredientes e o da pontuação
'''bash
lock_ingrediente = threading.Lock()
lock_pontuacao = threading.Lock()
'''
