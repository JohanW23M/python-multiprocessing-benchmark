#  Python Multiprocessing Benchmark

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Performance](https://img.shields.io/badge/Performance-Testing-success?style=for-the-badge)

Este repositorio contiene una Prueba de Concepto (PoC) diseñada para evaluar la eficiencia del procesamiento paralelo frente al secuencial en Python para tareas intensivas de CPU (*CPU-bound*), mitigando las limitaciones impuestas por el *Global Interpreter Lock (GIL)*.

##  Objetivo del Análisis
Cuantificar el impacto del *overhead* de coordinación en el modelo de multiprocesamiento nativo de Python y determinar el **Speedup** y la **Eficiencia** alcanzados en función de la topología del procesador local.

##  Metodología
Se definió una carga de trabajo matemática intensiva utilizando la *Floating Point Unit (FPU)* (`math.sqrt`, `math.sin`, `math.cos`) iterada `10,000,000` de veces para someter a la CPU a *stress-testing*.
* **Baseline Secuencial:** Ejecución en un único hilo para establecer la línea base de latencia.
* **Modelo Paralelo:** Distribución de la carga mediante `multiprocessing.Pool` particionando el trabajo entre todos los núcleos lógicos detectados.

## Conclusiones Técnicas del Experimento

### 1. Evasión del GIL y Reducción de Tiempos
El paralelismo explota la capacidad multi-núcleo mediante el paralelismo a nivel de proceso (PLP). Al particionar la carga en subconjuntos independientes, el tiempo de procesamiento se reduce de forma inversamente proporcional a los recursos físicos, logrando una optimización real frente a las restricciones del GIL en Python.

### 2. El Impacto del Overhead
El experimento demuestra que el multiprocesamiento no es "gratis". Existe latencia introducida por el sistema operativo al gestionar:
* Creación de procesos hijos.
* Serialización de datos (*Pickling*).
* Comunicación inter-procesos (*IPC*).
**Conclusión:** Si la granularidad de la tarea es insuficiente (valor de $N$ muy bajo), el costo temporal de administración superará la ganancia de velocidad, resultando en un Speedup ineficiente (< 1.0x).

### 3. Cuellos de Botella de Hardware
Durante la prueba se comprobó que el *Speedup* rara vez es lineal perfecto. Factores limitantes incluyen:
* Latencia de acceso a la jerarquía de memoria (Cachés L1/L2/L3).
* Contención de memoria RAM al recibir peticiones simultáneas de múltiples núcleos.

### 4. ¿Cuándo NO paralelizar en Python?
Este análisis confirma que la paralelización de procesos es contraproducente en:
* Algoritmos con alta dependencia de datos secuenciales.
* Tareas *I/O-bound* (lectura de disco/red), donde hilos concurrentes (`threading` o `asyncio`) son más eficientes y económicos.
* Cargas de cómputo triviales donde el *overhead* de orquestación destruye la ventaja de tiempo.
