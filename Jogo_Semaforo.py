import threading
import time
import random
import collections

class Semaforo:
    def __init__(self, inicial):
        self.sinal = inicial
        self.threads = collections.deque()
    def espera_condicional(self):
        while self.sinal == 0:
            time.sleep(0.01)
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
    def liberacao(self):
        self.sinal += 1
        if self.threads:
            self.threads.popleft()

# Definições de ingredientes e pedidos
INGREDIENTS = ["Tomate", "Queijo", "Massa", "Carne", "Alface", "Pão"]
MAX_INGREDIENTS = 5
ingredient_stock = {ingredient: MAX_INGREDIENTS for ingredient in INGREDIENTS}  # Estoque inicial de cada ingrediente
ingredient_replenish_time = 30  # Tempo em segundos para reabastecimento dos ingredientes

# Definições de pedidos
ORDERS = [
    {"Pizza": ["Massa", "Queijo", "Tomate"]},
    {"Hambúrguer": ["Pão", "Carne", "Alface"]},
    {"Salada": ["Alface", "Tomate", "Queijo"]}
]

# Configurações dos jogadores
player1_ingredients = {ingredient: 0 for ingredient in INGREDIENTS}  # Ingredientes coletados pelo Jogador 1
player2_ingredients = {ingredient: 0 for ingredient in INGREDIENTS}  # Ingredientes coletados pelo Jogador 2
player_scores = [0, 0]  # Pontuações dos jogadores

# Lock para controlar acesso aos ingredientes
semaforo_ingredientes = Semaforo(1)
semaforo_pontuacao = Semaforo(1)

def replenish_ingredients():
    """
    Função para reabastecer os ingredientes.
    """
    semaforo_ingredientes.captura()
    for ingredient in INGREDIENTS:
        ingredient_stock[ingredient] = MAX_INGREDIENTS
    print("Ingredientes reabastecidos.")
    semaforo_ingredientes.liberacao()

def collect_ingredient(player_ingredients, ingredient, player_id):
    """
    Função para coletar um ingrediente.
    """
    semaforo_ingredientes.captura()
    if ingredient_stock[ingredient] > 0:
        print(f"Jogador {player_id} está tentando coletar {ingredient}")
        player_ingredients[ingredient] += 1
        ingredient_stock[ingredient] -= 1
        time.sleep(1)
        print(f"Jogador coletou {ingredient}. Estoque restante: {ingredient_stock[ingredient]}")
    else:
        print(f"Ingrediente {ingredient} está fora de estoque.")
    semaforo_ingredientes.liberacao()

def complete_order(player_id, player_ingredients):
    """
    Função para completar um pedido.
    """
    order = random.choice(ORDERS)  # Escolhe um pedido aleatório
    order_name = list(order.keys())[0]
    order_ingredients = order[order_name]
    
    semaforo_pontuacao.captura()
    if all(player_ingredients[ingredient] > 0 for ingredient in order_ingredients):
        for ingredient in order_ingredients:
            player_ingredients[ingredient] -= 1  # Remove os ingredientes usados
        player_scores[player_id - 1] += 1  # Incrementa a pontuação do jogador
        print(f"Jogador {player_id} completou um pedido de {order_name}! Pontuação: {player_scores[player_id - 1]}")
    semaforo_pontuacao.liberacao()

def player_thread(player_id, player_ingredients, start_time):
    """
    Thread que representa as ações de um jogador.
    """
    while time.time() - start_time < 30.0:
        # Simular coleta de ingredientes
        ingredient = random.choice(INGREDIENTS)
        collect_ingredient(player_ingredients, ingredient, player_id)
        # Tentar completar um pedido
        complete_order(player_id, player_ingredients)
        time.sleep(random.uniform(0.5, 1.5))  # Simular tempo de ação do jogador

def game():
    """
    Função principal do jogo.
    """

    start_time = time.time()

    # Iniciar threads dos jogadores
    player1 = threading.Thread(target=player_thread, args=(1, player1_ingredients, start_time))
    player2 = threading.Thread(target=player_thread, args=(2, player2_ingredients, start_time))
    
    player1.start()
    player2.start()
    
    while time.time() - start_time < 30.0:  # Executar o jogo por 5 minutos (300 segundos)
        time.sleep(ingredient_replenish_time)  # Esperar pelo tempo de reabastecimento
        replenish_ingredients()  # Reabastecer os ingredientes
    
    #player1.join()  # Esperar a thread do jogador 1 terminar
    #player2.join()  # Esperar a thread do jogador 2 terminar
    
    print("Fim do jogo")
    print(f"Pontuação do Jogador 1: {player_scores[0]}")
    print(f"Pontuação do Jogador 2: {player_scores[1]}")
    print(f"Inventário do Jogador 1: {player1_ingredients}")
    print(f"Inventário do Jogador 2: {player2_ingredients}")

if __name__ == "__main__":
    game()
