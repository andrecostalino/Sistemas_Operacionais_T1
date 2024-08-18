# Trabalho Sistemas Microprocessados
Esse trabalho consiste em um jogo no qual ocorre condições de corrida que são solucionadas de formas variadas.

## Vídeo Execução do Jogo

[![Drawing-Recognition-Model](https://drive.google.com/file/d/1fsVVw9y0tIyq87rE7STVBvSgw9dCU8UV/view?usp=sharing)]

## O Jogo
Ele consiste numa competição entre dois cozinheiros que trabalham em um restaurante. Ambos tem como objetivo completar o máximo de pratos possível dentre os que estão presentes no cardápio do restaurante. Os cozinheiros dividem a mesma dispensa, e essa não pode ser acessada por ambos simultaneamente, logo parte da competição é a utilização eficiente do tempo e ingredientes a disposição para atingir o objetivo de três pontos antes do oponenete, vencendo o jogo.

### Cardapio
- Burrito: Feijão, Queijo e Carne
- Hámburguer: Pão, Queijo e Carne
- Salada: Alface, Tomate e Queijo

## Condições de Corrida
O jogo possui duas regiões críticas nas quais podem ocorrer condições de corrida, a dispensa compartilhada e a lista com as pontuações dos jogadores. Esses espaços não podem ser acessados simultaneamente, para que não ocorra nenhuma coleta ou escrita de dados equivocados nelas. As condições de corrida foram solucionadas de três formas diferentes: 
1.Lock
2.Semáforo
3.Monitor
  
### Lock
A solução por lock consite na criação de duas locks no princípio do jogo, o lock dos ingredientes e o da pontuação. Essas locks são provenientes da função Lock da biblioteca threading, nativa do Python.

```python
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

```python
class Semaforo:
    def __init__(self, inicial):
        self.sinal = inicial
        self.threads = collections.deque()
    #Espera pela liberação
    def espera_condicional(self):
        while self.sinal == 0:
            time.sleep(0.01)
    #Captura do semáforo pela thread
    def captura(self):
        while True:
            self.espera_condicional()
            if self.sinal > 0:
                self.sinal -= 1
                return
            else:
                self.threads.append(threading.current_thread())
                while threading.current_thread() in self.threads:
                    time.sleep(0.01)
    #Liberação do semáforo pela thread
    def liberacao(self):
        self.sinal += 1
        if self.threads:
            self.threads.popleft()
```

```python
def reposicao():
    semaforo_ingredientes.captura()
    for ingrediente in Ingredientes:
        dispensa[ingrediente] = dispensa_cheia
    print("Ingredientes reabastecidos.")
    semaforo_ingredientes.liberacao()
```

### Monitor
Funciona de forma muito similar aos anteriores em relação ao seu comportamento com as regiões críticas e, assim como o semáforo, precisa de uma classe para ser utilizado. Para implementação de seus recursos de espera pela liberação e da notificação as outras threads de quando este foi liberado, foi utilizada a função Condition() da biblioteca threading.

```python
#Classe Monitor
class Monitor:
    def __init__(self):
        self.ocupado = False
        self.monitor = threading.Condition()
    #Funções de captura e liberação da classe monitor
    def captura(self):
        with self.monitor:
            while self.ocupado:
                self.monitor.wait()
            self.ocupado = True
    def liberacao(self):
        with self.monitor:
            self.ocupado = False
            self.monitor.notify()
```

```python
def reposicao():
    monitor_ingredientes.captura()
    for ingrediente in Ingredientes:
        dispensa[ingrediente] = dispensa_cheia
    print("Ingredientes reabastecidos.")
    monitor_ingredientes.liberacao()
```

## Jogadores
Ambos os jogadores estão sendo simulados nesse jogo por meio de threads. Elas são implementadas a partir da função Thread() da biblioteca threading e são nelas em que as funções de coleta de ingredientes e compleção de pedidos são chamadas, além das devidas manipulações da dispensa e estoque intenor de ingredientes de cada jogador.

```python
def thread_jogador(id_jogador, ingredientes_jogador):
    #Thread jogador
    ls_ingrediente = 0
    ls_pedidos = 0
    while True:
        # Simular coleta de ingredientes
        ingrediente = script_ingredientes[ls_ingrediente].rstrip('\n')
        ls_ingrediente += 1
        coleta_ingredientes(ingredientes_jogador, ingrediente, id_jogador)
        if 3 in pontuacao_jogadores:
            break
        # Tentar completar um pedido
        completar_pedido(id_jogador, ingredientes_jogador, ls_pedidos)
        if ls_pedidos <= 1:
            ls_pedidos += 1
        else:
            ls_pedidos = 0
        time.sleep(0.1)  # Simular tempo de ação do jogador
```

## Utilização do jogo
Para que o jogo funcione em sua máquina, é necessário que esteja instalada alguma versão da linguagem Python. A partir disso, basta que sejam executados os seguintes comandos:

```bash
git clone https://github.com/andrecostalino/Sistemas_Operacionais_T1
```
```bash
cd .\Sistemas_Operacionais_T1\
```
```bash
python .\Jogo_Exclusao_Mutua.py
```
```bash
python .\Jogo_Monitor.py
```
```bash
python .\Jogo_Semaforo.py
```
