import threading
import time
import random

# Definições de ingredientes e pedidos
INGREDIENTS = ["Tomate", "Queijo", "Massa", "Carne", "Alface", "Pão"]
MAX_INGREDIENTS = 5
ingredient_stock = {ingredient: MAX_INGREDIENTS for ingredient in INGREDIENTS}
ingredient_replenish_time = 30  # Segundos

# Definições de pedidos
ORDERS = [
    {"Pizza": ["Massa", "Queijo", "Tomate"]},
    {"Hambúrguer": ["Pão", "Carne", "Alface"]},
    {"Salada": ["Alface", "Tomate", "Queijo"]}
]

# Configurações dos jogadores
player1_ingredients = {ingredient: 0 for ingredient in INGREDIENTS}
player2_ingredients = {ingredient: 0 for ingredient in INGREDIENTS}
player_scores = [0, 0]

# Lock para controlar acesso aos ingredientes
ingredient_lock = threading.Lock()
score_lock = threading.Lock()

def replenish_ingredients():
    with ingredient_lock:
        for ingredient in INGREDIENTS:
            ingredient_stock[ingredient] = MAX_INGREDIENTS
        print("Ingredientes reabastecidos.")

def collect_ingredient(player_ingredients, ingredient):
    with ingredient_lock:
        if ingredient_stock[ingredient] > 0:
            player_ingredients[ingredient] += 1
            ingredient_stock[ingredient] -= 1
            print(f"Jogador coletou {ingredient}. Estoque restante: {ingredient_stock[ingredient]}")
        else:
            print(f"Ingrediente {ingredient} está fora de estoque.")

def complete_order(player_id, player_ingredients):
    order = random.choice(ORDERS)
    order_name = list(order.keys())[0]
    order_ingredients = order[order_name]
    
    with score_lock:
        if all(player_ingredients[ingredient] > 0 for ingredient in order_ingredients):
            for ingredient in order_ingredients:
                player_ingredients[ingredient] -= 1
            player_scores[player_id - 1] += 1
            print(f"Jogador {player_id} completou um pedido de {order_name}! Pontuação: {player_scores[player_id - 1]}")
        else:
            print(f"Jogador {player_id} não tem ingredientes suficientes para completar um pedido de {order_name}.")

def player_thread(player_id, player_ingredients):
    while True:
        # Simular coleta de ingredientes
        ingredient = random.choice(INGREDIENTS)
        collect_ingredient(player_ingredients, ingredient)
        # Tentar completar um pedido
        complete_order(player_id, player_ingredients)
        time.sleep(random.uniform(0.5, 1.5))  # Simular tempo de ação do jogador

def game():
    # Iniciar threads dos jogadores
    player1 = threading.Thread(target=player_thread, args=(1, player1_ingredients))
    player2 = threading.Thread(target=player_thread, args=(2, player2_ingredients))
    
    player1.start()
    player2.start()
    
    start_time = time.time()
    
    while time.time() - start_time < 300:  # Executar o jogo por 5 minutos
        time.sleep(ingredient_replenish_time)
        replenish_ingredients()
    
    player1.join()
    player2.join()
    
    print("Fim do jogo")
    print(f"Pontuação do Jogador 1: {player_scores[0]}")
    print(f"Pontuação do Jogador 2: {player_scores[1]}")
    print(f"Inventário do Jogador 1: {player1_ingredients}")
    print(f"Inventário do Jogador 2: {player2_ingredients}")

if __name__ == "__main__":
    game()
