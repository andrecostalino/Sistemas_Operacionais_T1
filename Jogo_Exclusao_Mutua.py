import threading
import time
import random

#Leitura do script dos ingredientes
file = open("Script_Ingredientes.txt", "r")
script_ingredientes = file.readlines()
file.close()

# Definições de pedidos
Cardapio = [
    {"Burrito": ["Feijao", "Queijo", "Carne"]},
    {"Hambúrguer": ["Pao", "Carne", "Alface"]},
    {"Salada": ["Alface", "Tomate", "Queijo"]}
]

#Tempo reposicao ingredientes
tempo_reposicao = 20

# Definições de ingredientes e pedidos
Ingredientes = ["Tomate", "Queijo", "Feijao", "Carne", "Alface", "Pao"]
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
    # Reabastecimento dos ingredientes (Neste momento a dispensa também é regulada por um semáforo)
    with lock_ingrediente:
        for ingrediente in Ingredientes:
            dispensa[ingrediente] = dispensa_cheia
        print("Ingredientes reabastecidos.")

def coleta_ingredientes(ingredientes_jogador, ingrediente, id_jogador):
    """Os jogadores adicionam uma unidade de um ingrediente em específico a sua dispensa,
    tendo uma sinalização posterior disso."""
    print(f"Jogador {id_jogador} está aguardando a liberação da dispensa")
    with lock_ingrediente:
        if dispensa[ingrediente] > 0:
            print(f"Jogador {id_jogador} está tentando coletar {ingrediente}")
            ingredientes_jogador[ingrediente] += 1
            dispensa[ingrediente] -= 1
            time.sleep(1)
            print(f"Jogador coletou {ingrediente}. Estoque restante: {dispensa[ingrediente]}")
        else:
            # Caso não haja ingrediente disponível ele sinaliza nos logs
            print(f"Ingrediente {ingrediente} está fora de estoque.")

def completar_pedido(id_jogador, ingredientes_jogador, escolha_pedido):
    pedido = Cardapio[escolha_pedido]  # Seleciona um pedido baseando-se num script criado
    nome_pedido = list(pedido.keys())[0]
    ingredientes_pedido = pedido[nome_pedido]
    
    print(f"O jogador {id_jogador} está tentando acessar a tabela de pontuação")
    with lock_pontuacao:
        # Verifica se o jogador tem todos os ingredientes necessários
        if all(ingredientes_jogador[ingrediente] > 0 for ingrediente in ingredientes_pedido):
            for ingrediente in ingredientes_pedido:
                ingredientes_jogador[ingrediente] -= 1  # Remove os ingredientes usados
            pontuacao_jogadores[id_jogador - 1] += 1  # Incrementa a pontuação do jogador
            print(f"Jogador {id_jogador} completou um pedido de {nome_pedido}! Pontuação: {pontuacao_jogadores[id_jogador - 1]}")

def thread_jogador(id_jogador, ingredientes_jogador):
    """Threads dos jogadores. Seguem os scripts pré-determinados e interrompem quando um dos jogadores
    atinge a pontuação 3."""
    ls_ingrediente = 0
    ls_pedidos = 0
    while True:
        # Simular coleta de ingredientes
        ingredient = script_ingredientes[ls_ingrediente].rstrip('\n')
        ls_ingrediente += 1
        coleta_ingredientes(ingredientes_jogador, ingredient, id_jogador)
        if 3 in pontuacao_jogadores:
            break
        # Tentar completar um pedido
        completar_pedido(id_jogador, ingredientes_jogador, ls_pedidos)
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
    player1 = threading.Thread(target=thread_jogador, args=(1, ingredientes_jogador1))
    player2 = threading.Thread(target=thread_jogador, args=(2, ingredientes_jogador2))
    
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
    print(f"Inventário do Jogador 1: {ingredientes_jogador1}")
    print(f"Inventário do Jogador 2: {ingredientes_jogador2}")
    fim_cronometro = time.time()
    print(f"Finalizado após {fim_cronometro - inicio_cronometro} segundos")

if __name__ == "__main__":
    game()
