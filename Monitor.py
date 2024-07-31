import threading
import time

class Monitor:
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

# Função worker que simula a tarefa das threads
def worker(monitor, worker_id):
    print(f"Worker {worker_id} está esperando para adquirir o monitor")
    monitor.acquire()
    print(f"Worker {worker_id} adquiriu o monitor")
    # Simula alguma tarefa
    time.sleep(1)
    print(f"Worker {worker_id} está liberando o monitor")
    monitor.release()

if __name__ == "__main__":
    # Cria um monitor com um contador inicial de 2
    monitor = Monitor(2)

    # Cria e inicia múltiplas threads de trabalhadores
    threads = []
    for i in range(5):
        thread = threading.Thread(target=worker, args=(monitor, i))
        threads.append(thread)
        thread.start()

    # Espera todas as threads terminarem
    for thread in threads:
        thread.join()

    print("Todos os workers terminaram.")
