#Universidad del Valle de Guatemala
#Algoritmos y Estructuras de datos
#Sección 40
#Lingna Chen - 23173

import simpy
import random
import statistics
import matplotlib.pyplot as plt

# Configuración inicial y constantes de simulación
CAPACIDAD_RAM = 100
VELOCIDAD_CPU = 1
NUM_PROCESOS = 200
INTERVALO_PROCESOS = 10
TIEMPO_SIMULACION = 100

# Variables para estadísticas
tiempos = []

class Proceso:
    def __init__(self, env, id, sistema_operativo):
        self.env = env
        self.id = id
        self.memoria_requerida = random.randint(1, 10)
        self.instrucciones = random.randint(1, 10)
        self.sistema_operativo = sistema_operativo
        self.tiempo_llegada = env.now
        self.action = env.process(self.run())  

    def run(self):
        print(f'[{self.env.now}] Proceso {self.id}: Creado, requiere {self.memoria_requerida} unidades de RAM.')
        yield self.sistema_operativo.RAM.get(self.memoria_requerida)  
        print(f'[{self.env.now}] Proceso {self.id}: RAM asignada.')

        while self.instrucciones > 0:
            with self.sistema_operativo.CPU.request() as req:
                yield req
                yield self.env.timeout(1)  
                self.instrucciones -= VELOCIDAD_CPU
                print(f'[{self.env.now}] Proceso {self.id}: Ejecutando, restan {self.instrucciones} instrucciones.')

            if self.instrucciones > 0:
                yield self.env.timeout(1)  
                print(f'[{self.env.now}] Proceso {self.id}: Esperando por I/O.')

        self.sistema_operativo.RAM.put(self.memoria_requerida)  
        print(f'[{self.env.now}] Proceso {self.id}: Terminado.')
        tiempos.append(self.env.now - self.tiempo_llegada)

class SistemaOperativo:
    def __init__(self, env):
        self.env = env
        self.RAM = simpy.Container(env, init=CAPACIDAD_RAM, capacity=CAPACIDAD_RAM)
        self.CPU = simpy.Resource(env, capacity=1)

def generador_procesos(env, sistema_operativo):
    for i in range(NUM_PROCESOS):
        Proceso(env, i, sistema_operativo)
        yield env.timeout(random.expovariate(1.0 / INTERVALO_PROCESOS))

env = simpy.Environment()
sistema_operativo = SistemaOperativo(env)
env.process(generador_procesos(env, sistema_operativo))
env.run(until=TIEMPO_SIMULACION)

uso_ram = []  

class Proceso:
    ...

class SistemaOperativo:
    def __init__(self, env):
        self.env = env
        self.RAM = simpy.Container(env, init=CAPACIDAD_RAM, capacity=CAPACIDAD_RAM)
        self.CPU = simpy.Resource(env, capacity=1)
        self.env.process(self.monitor_ram())  #Iniciar

    def monitor_ram(self):
        while True:
            uso_ram.append((self.env.now, self.RAM.level))
            yield self.env.timeout(1)  # Actualiza cada unidad de tiempo


# Estadísticas
if tiempos:
    print(f'Tiempo promedio: {statistics.mean(tiempos)}')
    if len(tiempos) > 1:
        print(f'Desviación estándar: {statistics.stdev(tiempos)}')
else:
    print("No se completaron procesos para calcular estadísticas.")
