import multiprocessing
import os
import time
import math
from multiprocessing import Pool

# Configuración de la carga de trabajo
N = 10_000_000 

def tarea_intensiva(i: int) -> float:
    """Simulación de tarea CPU-bound utilizando la FPU."""
    return math.sqrt(i) * math.sin(i) + math.cos(i)

def ejecutar_paralelo(n: int, num_procesos: int):
    with Pool(processes=num_procesos) as pool:
        return pool.map(tarea_intensiva, range(1, n + 1))

if __name__ == "__main__":
    print("--- Benchmark de Procesamiento: Secuencial vs Paralelo ---")
    n_nucleos = multiprocessing.cpu_count()
    print(f"Sistema Operativo: {os.name} | Núcleos lógicos: {n_nucleos}")
    
    # 1. Ejecución Secuencial
    print(f"\n[1] Iniciando fase secuencial (N = {N})...")
    t0_seq = time.perf_counter()
    resultados_seq = [tarea_intensiva(i) for i in range(1, N + 1)]
    t1_seq = time.perf_counter()
    tiempo_secuencial = t1_seq - t0_seq
    print(f"Tiempo de ejecución secuencial: {tiempo_secuencial:.4f} s")

    # 2. Ejecución Paralela
    print(f"\n[2] Lanzando ejecución paralela con {n_nucleos} procesos...")
    t0_par = time.perf_counter()
    resultados_par = ejecutar_paralelo(N, num_procesos=n_nucleos)
    t1_par = time.perf_counter()
    tiempo_paralelo = t1_par - t0_par
    print(f"Tiempo de ejecución paralela: {tiempo_paralelo:.4f} s")

    # 3. Métricas de Rendimiento
    print("\n--- Resultados Finales ---")
    speedup = tiempo_secuencial / tiempo_paralelo
    eficiencia = (speedup / n_nucleos) * 100
    print(f"Speedup calculado: {speedup:.2f}x")
    print(f"Eficiencia de paralelización: {eficiencia:.2f}%")
