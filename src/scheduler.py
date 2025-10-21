"""
Módulo que define los algoritmos de planificación de CPU.
Incluye una clase base abstracta y las implementaciones de FCFS y Round-Robin.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
from copy import deepcopy
from proceso import Proceso

# Tipo para las entradas del diagrama de Gantt
GanttEntry = Tuple[str, int, int]  # (pid, tiempo_inicio, tiempo_fin)


class Scheduler(ABC):
    """
    Clase abstracta que define la interfaz para los algoritmos de planificación.
    """
    
    @abstractmethod
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        """
        Planifica la ejecución de un conjunto de procesos.
        
        Args:
            procesos (List[Proceso]): Lista de procesos a planificar
        
        Returns:
            List[GanttEntry]: Diagrama de Gantt con tuplas (pid, tiempo_inicio, tiempo_fin)
        """
        pass


class FCFSScheduler(Scheduler):
    """
    Implementa el algoritmo First-Come, First-Served (FCFS).
    Los procesos se ejecutan en el orden en que llegan, sin interrupciones.
    """
    
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        """
        Planifica procesos usando FCFS: el primero en llegar es el primero en ejecutarse.
        
        Args:
            procesos (List[Proceso]): Lista de procesos a planificar
        
        Returns:
            List[GanttEntry]: Diagrama de Gantt con la secuencia de ejecución
        """
        if not procesos:
            return []
        
        # Hacer copias profundas de los procesos para no modificar los originales
        procesos_copia = [deepcopy(p) for p in procesos]
        
        # Ordenar por tiempo de llegada (aunque por defecto todos llegan a tiempo 0)
        procesos_copia.sort(key=lambda p: p.tiempo_llegada)
        
        gantt = []
        tiempo_actual = 0
        
        for proceso in procesos_copia:
            # Si el proceso aún no ha llegado, avanzar el tiempo
            if tiempo_actual < proceso.tiempo_llegada:
                tiempo_actual = proceso.tiempo_llegada
            
            # Establecer tiempo de inicio si es la primera vez que se ejecuta
            if proceso.tiempo_inicio is None:
                proceso.tiempo_inicio = tiempo_actual
            
            # Ejecutar el proceso completamente (FCFS no tiene interrupciones)
            tiempo_fin = tiempo_actual + proceso.duracion
            gantt.append((proceso.pid, tiempo_actual, tiempo_fin))
            
            # Actualizar el tiempo de finalización del proceso
            proceso.tiempo_fin = tiempo_fin
            proceso.tiempo_restante = 0
            
            # Avanzar el tiempo actual
            tiempo_actual = tiempo_fin
        
        # Actualizar los procesos originales con los tiempos calculados
        for i, proceso_original in enumerate(procesos):
            proceso_original.tiempo_inicio = procesos_copia[i].tiempo_inicio
            proceso_original.tiempo_fin = procesos_copia[i].tiempo_fin
            proceso_original.tiempo_restante = 0
        
        return gantt


class RoundRobinScheduler(Scheduler):
    """
    Implementa el algoritmo Round-Robin con quantum configurable.
    Los procesos se ejecutan por turnos, cada uno recibe un quantum de tiempo.
    """
    
    def __init__(self, quantum: int = 4):
        """
        Inicializa el planificador Round-Robin.
        
        Args:
            quantum (int): Tiempo máximo de CPU asignado a cada proceso en cada turno
        
        Raises:
            ValueError: Si el quantum no es positivo
        """
        if quantum <= 0:
            raise ValueError("El quantum debe ser un entero positivo")
        self.quantum = quantum
    
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        """
        Planifica procesos usando Round-Robin con el quantum especificado.
        
        Args:
            procesos (List[Proceso]): Lista de procesos a planificar
        
        Returns:
            List[GanttEntry]: Diagrama de Gantt con la secuencia de ejecución
        """
        if not procesos:
            return []
        
        # Hacer copias profundas de los procesos para no modificar los originales
        procesos_copia = [deepcopy(p) for p in procesos]
        
        # Crear una cola circular de procesos pendientes
        cola = procesos_copia.copy()
        gantt = []
        tiempo_actual = 0
        
        while cola:
            proceso = cola.pop(0)  # Tomar el primer proceso de la cola
            
            # Si el proceso aún no ha llegado, avanzar el tiempo
            if tiempo_actual < proceso.tiempo_llegada:
                tiempo_actual = proceso.tiempo_llegada
            
            # Establecer tiempo de inicio si es la primera vez que se ejecuta
            if proceso.tiempo_inicio is None:
                proceso.tiempo_inicio = tiempo_actual
            
            # Determinar cuánto tiempo ejecutará este proceso en este ciclo
            tiempo_ejecucion = min(self.quantum, proceso.tiempo_restante)
            tiempo_fin = tiempo_actual + tiempo_ejecucion
            
            # Registrar la ejecución en el diagrama de Gantt
            gantt.append((proceso.pid, tiempo_actual, tiempo_fin))
            
            # Actualizar el tiempo restante del proceso
            proceso.tiempo_restante -= tiempo_ejecucion
            tiempo_actual = tiempo_fin
            
            # Si el proceso no ha terminado, volver a colocarlo al final de la cola
            if proceso.tiempo_restante > 0:
                cola.append(proceso)
            else:
                # El proceso ha finalizado
                proceso.tiempo_fin = tiempo_actual
        
        # Actualizar los procesos originales con los tiempos calculados
        for i, proceso_original in enumerate(procesos):
            proceso_original.tiempo_inicio = procesos_copia[i].tiempo_inicio
            proceso_original.tiempo_fin = procesos_copia[i].tiempo_fin
            proceso_original.tiempo_restante = 0
        
        return gantt
