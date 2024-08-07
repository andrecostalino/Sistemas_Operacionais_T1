import threading
import time
import random

# Definições de pedidos
Cardapio = [
    {"Burrito": ["Feijao", "Queijo", "Tomate"]},
    {"Hambúrguer": ["Pão", "Carne", "Alface"]},
    {"Salada": ["Alface", "Tomate", "Queijo"]}
]

#Tempo reposicao ingredientes
ingredient_replenish_time = 30  

# Definições de ingredientes e pedidos
Ingredientes = ["Tomate", "Queijo", "Feijao", "Carne", "Alface", "Pão"]
dispensa_cheia = 5
dispensa = {ingrediente: dispensa_cheia for ingrediente in Ingredientes}  # Estoque inicial de cada ingrediente

# Configurações dos jogadores
ingredientes_jogador1 = {ingrediente: 0 for ingrediente in Ingredientes}  # Ingredientes coletados pelo Jogador 1
ingredientes_jogador2 = {ingrediente: 0 for ingrediente in Ingredientes}  # Ingredientes coletados pelo Jogador 2
pontuacao_jogadores = [0, 0]  # Pontuações dos jogadores

# Lock para controlar acesso aos ingredientes
lock_ingrediente = threading.Lock()
lock_pontuacao = threading.Lock()

def reposicao():
    #Reposição ingredientes
    with lock_ingrediente:
        for ingrediente in Ingredientes:
            dispensa[ingrediente] = dispensa_cheia
        print("Ingredientes reabastecidos.")

def coleta_ingredientes(ingredientes_jogador, ingrediente, id_jogador):
    #Coleta ingredientes
    with lock_ingrediente:
        if dispensa[ingrediente] > 0:
            print(f"Jogador {id_jogador} está tentando coletar {ingrediente}")
            ingredientes_jogador[ingrediente] += 1
            dispensa[ingrediente] -= 1
            time.sleep(1)
            print(f"Jogador coletou {ingrediente}. Estoque restante: {dispensa[ingrediente]}")
        else:
            print(f"Ingrediente {ingrediente} está fora de estoque.")

def completar_pedido(id_jogador, ingredientes_jogador):
    #Pedido sendo completo pelo jogador
    pedido = random.choice(Cardapio)  # Escolhe um pedido aleatório
    nome_pedido = list(pedido.keys())[0]
    ingredientes_pedido = pedido[nome_pedido]
    
    with lock_pontuacao:
        # Verifica se o jogador tem todos os ingredientes necessários
        if all(ingredientes_jogador[ingrediente] > 0 for ingrediente in ingredientes_pedido):
            for ingrediente in ingredientes_pedido:
                ingredientes_jogador[ingrediente] -= 1  # Remove os ingredientes usados
            pontuacao_jogadores[id_jogador - 1] += 1  # Incrementa a pontuação do jogador
            print(f"Jogador {id_jogador} completou um pedido de {nome_pedido}! Pontuação: {pontuacao_jogadores[id_jogador - 1]}")

def thread_jogador(id_jogador, ingredientes_jogador):
    #Montagem da thread de cada jogador
    while 5 not in pontuacao_jogadores:
        # Simular coleta de ingredientes
        ingredient = random.choice(Ingredientes)
        coleta_ingredientes(ingredientes_jogador, ingredient, id_jogador)
        # Tentar completar um pedido
        completar_pedido(id_jogador, ingredientes_jogador)
        time.sleep(random.uniform(0.5, 1.5))  # Simular tempo de ação do jogador

def game():
    
    # Iniciar threads dos jogadores
    player1 = threading.Thread(target=thread_jogador, args=(1, ingredientes_jogador1))
    player2 = threading.Thread(target=thread_jogador, args=(2, ingredientes_jogador2))
    
    player1.start()
    player2.start()
    
    while 5 not in pontuacao_jogadores:  # Executar o jogo por 5 minutos (300 segundos)
        time.sleep(ingredient_replenish_time)  # Esperar pelo tempo de reabastecimento
        reposicao()  # Reabastecer os ingredientes
    
    player1.join()  # Esperar a thread do jogador 1 terminar
    player2.join()  # Esperar a thread do jogador 2 terminar
    
    print("Fim do jogo")
    print(f"Pontuação do Jogador 1: {pontuacao_jogadores[0]}")
    print(f"Pontuação do Jogador 2: {pontuacao_jogadores[1]}")
    print(f"Inventário do Jogador 1: {ingredientes_jogador1}")
    print(f"Inventário do Jogador 2: {ingredientes_jogador2}")

if __name__ == "__main__":
    game()
