import threading
import time
import collections

#Leitura do script dos ingredientes
file = open("Script_Ingredientes.txt", "r")
script_ingredientes = file.readlines()
file.close()

#Classe Semáforo
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

#Possíveis pedidos
Cardapio = [{"Burrito": ["Carne", "Queijo", "Feijao"]}, 
           {"Hambúrguer": ["Pao", "Carne", "Alface"]}, 
           {"Salada": ["Alface", "Tomate", "Queijo"]}]

# Definições de ingredientes e pedidos
Ingredientes = ["Tomate", "Queijo", "Feijao", "Carne", "Alface", "Pao"]
dispensa_cheia = 5
dispensa = {ingrediente: dispensa_cheia for ingrediente in Ingredientes}  # Estoque inicial de cada ingrediente

#Tempo para reposição dos ingredientes
tempo_reposicao = 20

# Configurações dos jogadores
ingredientes_player1 = {ingrediente: 0 for ingrediente in Ingredientes}  # Ingredientes coletados pelo Jogador 1
ingredientes_player2 = {ingrediente: 0 for ingrediente in Ingredientes}  # Ingredientes coletados pelo Jogador 2
pontuacao_jogadores = [0, 0]  # Pontuações dos jogadores

# Semáforo que limita o acesso aos ingredientes e a lista de pontuação
semaforo_ingredientes = Semaforo(1)
semaforo_pontuacao = Semaforo(1)

def reposicao():
    # Reabastecimento dos ingredientes (Neste momento a dispensa também é regulada por um semáforo)
    semaforo_ingredientes.captura()
    for ingrediente in Ingredientes:
        dispensa[ingrediente] = dispensa_cheia
    print("Ingredientes reabastecidos.")
    semaforo_ingredientes.liberacao()

def coleta_ingrediente(ingredientes_player, ingrediente, id_jogador):
    """Os jogadores adicionam uma unidade de um ingrediente em específico a sua dispensa,
    tendo uma sinalização posterior disso."""
    print(f"Jogador {id_jogador} está aguardando a liberação da dispensa")
    semaforo_ingredientes.captura()
    if dispensa[ingrediente] > 0:
        print(f"Jogador {id_jogador} está tentando coletar {ingrediente}")
        ingredientes_player[ingrediente] += 1
        dispensa[ingrediente] -= 1
        time.sleep(1)
        print(f"Jogador {id_jogador} coletou {ingrediente}. Estoque restante: {dispensa[ingrediente]}")
    else:
        # Caso não haja ingrediente disponível ele sinaliza nos logs
        print(f"Ingrediente {ingrediente} está fora de estoque.")
    semaforo_ingredientes.liberacao()

def completar_pedido(id_jogador, ingredientes_player, escolha_pedido):
    pedido = Cardapio[escolha_pedido]  # Seleciona um pedido baseando-se num script criado
    nome_pedido = list(pedido.keys())[0]
    ingrediente_pedido = pedido[nome_pedido]
    
    print(f"O jogador {id_jogador} está tentando acessar a tabela de pontuação")
    semaforo_pontuacao.captura() # A lista de pontuações também é considerada uma região crítica
    # Verifica se o jogador tem todos os ingredientes necessários
    if all(ingredientes_player[ingrediente] > 0 for ingrediente in ingrediente_pedido):
        for ingrediente in ingrediente_pedido:
            ingredientes_player[ingrediente] -= 1  # Remove os ingredientes usados
        pontuacao_jogadores[id_jogador - 1] += 1  # Incrementa a pontuação do jogador
        print(f"Jogador {id_jogador} completou um pedido de {nome_pedido}! Pontuação: {pontuacao_jogadores[id_jogador - 1]}")
    semaforo_pontuacao.liberacao()

def thread_jogador(id_jogador, ingredientes_player):
    """Threads dos jogadores. Seguem os scripts pré-determinados e interrompem quando um dos jogadores
    atinge a pontuação 3."""
    ls_ingrediente = 0
    ls_pedidos = 0
    while True:
        # Simular coleta de ingredientes
        ingrediente = script_ingredientes[ls_ingrediente].rstrip('\n')
        ls_ingrediente += 1
        coleta_ingrediente(ingredientes_player, ingrediente, id_jogador)
        if 3 in pontuacao_jogadores:
            break
        # Tentar completar um pedido
        completar_pedido(id_jogador, ingredientes_player, ls_pedidos)
        if ls_pedidos <= 1:
            ls_pedidos += 1
        else:
            ls_pedidos = 0
        time.sleep(0.1)  # Simular tempo de ação do jogador

def game():
    #Cronometragem do jogo
    inicio_cronometro = time.time()
    inicio_cronometro_reposicao = time.time()

    # Iniciar threads dos jogadores
    player1 = threading.Thread(target=thread_jogador, args=(1, ingredientes_player1))
    player2 = threading.Thread(target=thread_jogador, args=(2, ingredientes_player2))
    
    player1.start()
    player2.start()
    
    while True:  
        cronometro_reposicao = time.time()
        if cronometro_reposicao - inicio_cronometro_reposicao >= tempo_reposicao:
            reposicao()  # Reabastecer os ingredientes]
            inicio_cronometro_reposicao = cronometro_reposicao
        if 3 in pontuacao_jogadores: # Encerra o jogo quando um jogador completa 3 pedidos
            break
    
    player1.join()  # Esperar a thread do jogador 1 terminar
    player2.join()  # Esperar a thread do jogador 2 terminar
    
    print("Fim do jogo")
    print(f"Pontuação do Jogador 1: {pontuacao_jogadores[0]}")
    print(f"Pontuação do Jogador 2: {pontuacao_jogadores[1]}")
    print(f"Inventário do Jogador 1: {ingredientes_player1}")
    print(f"Inventário do Jogador 2: {ingredientes_player2}")
    fim_cronometro = time.time()
    print(f"Finalizado após {fim_cronometro - inicio_cronometro} segundos")

if __name__ == "__main__":
    game()
