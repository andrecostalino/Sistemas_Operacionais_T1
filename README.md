# Trabalho Sistemas Microprocessados
Esse trabalho consiste em um jogo no qual ocorre condições de corrida que são solucionadas de formas variadas.

## O Jogo
Ele consiste numa competição entre dois cozinheiros que trabalham em um restaurante. Ambos tem como objetivo completar o máximo de pratos possível dentre os que estão presentes no cardápio do restaurante. Os cozinheiros dividem a mesma dispensa, e essa não pode ser acessada por ambos simultaneamente, logo parte da competição é a utilização eficiente do tempo e ingredientes a disposição para atingir o objetivo de três pontos antes do oponenete, vencendo o jogo.

### Cardapio
- Burrito: Feijão, Queijo e Carne
- Hámburguer: Pão, Queijo e Carne
- Salada: Alface, Tomate e Queijo
- 
## Condições de Corrida
O jogo possui duas regiões críticas nas quais podem ocorrer condições de corrida, a dispensa compartilhada e a lista com as pontuações dos jogadores. Esses espaços não podem ser acessados simultaneamente, para que não ocorra nenhuma coleta ou escrita de dados equivocados nelas. As condições de corrida foram solucionadas de três formas diferentes: 
1.Lock
2.Semáforo
3.Monitor
  
### Lock
A solução por lock consite na criação de dois locks no princípio do jogo, o lock dos ingredientes e o da pontuação

```bash
lock_ingrediente = threading.Lock()
lock_pontuacao = threading.Lock()
```
Para que sejam acessadas a dispensa e a lista de pontuação é necessário estar em posse de sua respectiva lock. Essas tentativas de capturá-la ocorrem nos momentos em que um ingrediente será coletado, reposto ou uma ordem será concluída. No exemplo abaixo pode ser visto o funcionamento dela no momento em que o jogo tenta reabastecar a dispensa de ingredientes:

```python
def reposicao():
    # Reabastecimento dos ingredientes (Neste momento a dispensa também é regulada por um semáforo)
    with lock_ingrediente:
        for ingrediente in Ingredientes:
            dispensa[ingrediente] = dispensa_cheia
        print("Ingredientes reabastecidos.")
```
Após a conclusão do processo, a lock é automaticamente liberada e fica, novamente, a disposição.

### Semáforo
Funciona de uma maneira muito similar a lock em relação a sua necessidade para manipulação da dispensa e lista de pontuação. Possui uma classe específica para ele, na qual podem ser encontrador os métodos para captura e liberação do semáforo, como pode ser visto abaixo


