import threading

class Semaphore:
    def __init__(self, initial):
        self.count = initial
        self.condition = threading.Condition()

    def acquire(self):
        with self.condition:
            while self.count == 0:
                self.condition.wait()
            self.count -= 1

    def release(self):
        with self.condition:
            self.count += 1
            self.condition.notify()

# Exemplo de uso do semáforo
def worker(semaphore, worker_id):
    print(f"Worker {worker_id} está esperando para adquirir o semáforo")
    semaphore.acquire()
    print(f"Worker {worker_id} adquiriu o semáforo")
    # Simula alguma tarefa
    time.sleep(1)
    print(f"Worker {worker_id} está liberando o semáforo")
    semaphore.release()

if __name__ == "__main__":
    import time

    # Cria um semáforo com um contador inicial de 2
    semaphore = Semaphore(2)

    # Cria e inicia múltiplas threads de trabalhadores
    threads = []
    for i in range(5):
        thread = threading.Thread(target=worker, args=(semaphore, i))
        threads.append(thread)
        thread.start()

    # Espera todas as threads terminarem
    for thread in threads:
        thread.join()

    print("Todos os workers terminaram.")
