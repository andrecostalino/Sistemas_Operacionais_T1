import threading
import time
import random
import collections

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
tempo_reposicao = 30  

# Configurações dos jogadores
ingredientes_player1 = {ingrediente: 0 for ingrediente in Ingredientes}  # Ingredientes coletados pelo Jogador 1
ingredientes_player2 = {ingrediente: 0 for ingrediente in Ingredientes}  # Ingredientes coletados pelo Jogador 2
pontuacao_jogadores = [0, 0]  # Pontuações dos jogadores

# Lock para controlar acesso aos ingredientes
semaforo_ingredientes = Semaforo(1)
semaforo_pontuacao = Semaforo(1)

def reposicao():
    #Reabastecimento dos ingredientes
    semaforo_ingredientes.captura()
    for ingrediente in Ingredientes:
        dispensa[ingrediente] = dispensa_cheia
    print("Ingredientes reabastecidos.")
    semaforo_ingredientes.liberacao()

def coleta_ingrediente(ingredientes_player, ingrediente, id_jogador):
    #Coleta ingredientes
    semaforo_ingredientes.captura()
    if dispensa[ingrediente] > 0:
        print(f"Jogador {id_jogador} está tentando coletar {ingrediente}")
        ingredientes_player[ingrediente] += 1
        dispensa[ingrediente] -= 1
        time.sleep(1)
        print(f"Jogador {id_jogador} coletou {ingrediente}. Estoque restante: {dispensa[ingrediente]}")
    else:
        print(f"Ingrediente {ingrediente} está fora de estoque.")
    semaforo_ingredientes.liberacao()

def completar_pedido(id_jogador, ingredientes_player, escolha_pedido):
    pedido = Cardapio[escolha_pedido]  # Escolhe um pedido aleatório
    nome_pedido = list(pedido.keys())[0]
    ingrediente_pedido = pedido[nome_pedido]
    
    semaforo_pontuacao.captura()
    if all(ingredientes_player[ingrediente] > 0 for ingrediente in ingrediente_pedido):
        for ingrediente in ingrediente_pedido:
            ingredientes_player[ingrediente] -= 1  # Remove os ingredientes usados
        pontuacao_jogadores[id_jogador - 1] += 1  # Incrementa a pontuação do jogador
        print(f"Jogador {id_jogador} completou um pedido de {nome_pedido}! Pontuação: {pontuacao_jogadores[id_jogador - 1]}")
    semaforo_pontuacao.liberacao()

def thread_jogador(id_jogador, ingredientes_player):
    #Thread jogador
    ls_ingrediente = 0
    ls_pedidos = 0
    while True:
        # Simular coleta de ingredientes
        ingrediente = script_ingredientes[ls_ingrediente].rstrip('\n')
        ls_ingrediente += 1
        coleta_ingrediente(ingredientes_player, ingrediente, id_jogador)
        # Tentar completar um pedido
        if 3 in pontuacao_jogadores:
            break
        completar_pedido(id_jogador, ingredientes_player, ls_pedidos)
        if ls_pedidos <= 1:
            ls_pedidos += 1
        else:
            ls_pedidos = 0
        time.sleep(0.1)  # Simular tempo de ação do jogador

def game():
    #Cronometragem do jogo
    inicio_cronometro = time.time()

    # Iniciar threads dos jogadores
    player1 = threading.Thread(target=thread_jogador, args=(1, ingredientes_player1))
    player2 = threading.Thread(target=thread_jogador, args=(2, ingredientes_player2))
    
    player1.start()
    player2.start()
    
    while True:  # Executar o jogo por 5 minutos (300 segundos)
        time.sleep(tempo_reposicao)  # Esperar pelo tempo de reabastecimento
        reposicao()  # Reabastecer os ingredientes
        if 3 in pontuacao_jogadores:
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
