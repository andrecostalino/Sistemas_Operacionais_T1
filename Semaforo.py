import time
import collections
import threading

class CustomSemaphore:
    def __init__(self, initial):
        self.count = initial
        self.waiting_threads = collections.deque()  # Fila para armazenar threads em espera

    def acquire(self):
        while True:
            self._lock()
            if self.count > 0:
                self.count -= 1
                return
            else:
                # Se não há recursos disponíveis, a thread entra na fila de espera
                self.waiting_threads.append(threading.current_thread())
                while threading.current_thread() in self.waiting_threads:
                    time.sleep(0.01)  # Evitar busy-waiting

    def release(self):
        self.count += 1
        if self.waiting_threads:
            # Remove a thread da fila de espera e notifica
            self.waiting_threads.popleft()

    def _lock(self):
        while self.count == 0:
            time.sleep(0.01)  # Espera até que o lock esteja disponível

    def _current_thread(self):
        # Retorna uma representação simples da thread atual
        return threading.current_thread()

# Função worker que simula a tarefa das threads
def worker(semaphore, worker_id):
    print(f"Worker {worker_id} está esperando para adquirir o semáforo")
    semaphore.acquire()
    print(f"Worker {worker_id} adquiriu o semáforo")
    # Simula alguma tarefa
    time.sleep(1)
    print(f"Worker {worker_id} está liberando o semáforo")
    semaphore.release()

if __name__ == "__main__":
    # Cria um semáforo com um contador inicial de 2
    semaphore = CustomSemaphore(2)

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
