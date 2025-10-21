"""
Pruebas unitarias para los algoritmos de planificación.
"""

import pytest
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from proceso import Proceso
from scheduler import FCFSScheduler, RoundRobinScheduler


class TestFCFSScheduler:
    """Tests para el planificador FCFS."""
    
    def test_fcfs_procesos_vacios(self):
        """Test: FCFS con lista vacía retorna lista vacía."""
        scheduler = FCFSScheduler()
        gantt = scheduler.planificar([])
        assert gantt == []
    
    def test_fcfs_un_proceso(self):
        """Test: FCFS con un solo proceso."""
        scheduler = FCFSScheduler()
        proceso = Proceso("P1", 10, 1)
        gantt = scheduler.planificar([proceso])
        
        assert len(gantt) == 1
        assert gantt[0] == ("P1", 0, 10)
    
    def test_fcfs_multiples_procesos(self):
        """Test: FCFS con múltiples procesos ejecuta en orden."""
        scheduler = FCFSScheduler()
        procesos = [
            Proceso("P1", 5, 1),
            Proceso("P2", 3, 2),
            Proceso("P3", 8, 1)
        ]
        
        gantt = scheduler.planificar(procesos)
        
        assert len(gantt) == 3
        assert gantt[0] == ("P1", 0, 5)
        assert gantt[1] == ("P2", 5, 8)
        assert gantt[2] == ("P3", 8, 16)
    
    def test_fcfs_actualiza_tiempos_procesos(self):
        """Test: FCFS actualiza tiempo_inicio y tiempo_fin en procesos."""
        scheduler = FCFSScheduler()
        procesos = [
            Proceso("P1", 5, 1),
            Proceso("P2", 3, 2)
        ]
        
        scheduler.planificar(procesos)
        
        assert procesos[0].tiempo_inicio == 0
        assert procesos[0].tiempo_fin == 5
        assert procesos[1].tiempo_inicio == 5
        assert procesos[1].tiempo_fin == 8
    
    def test_fcfs_no_modifica_procesos_originales_restante(self):
        """Test: FCFS actualiza tiempo_restante a 0."""
        scheduler = FCFSScheduler()
        procesos = [Proceso("P1", 10, 1)]
        
        scheduler.planificar(procesos)
        
        assert procesos[0].tiempo_restante == 0


class TestRoundRobinScheduler:
    """Tests para el planificador Round-Robin."""
    
    def test_rr_quantum_invalido(self):
        """Test: Quantum no positivo lanza ValueError."""
        with pytest.raises(ValueError, match="El quantum debe ser un entero positivo"):
            RoundRobinScheduler(quantum=0)
        
        with pytest.raises(ValueError, match="El quantum debe ser un entero positivo"):
            RoundRobinScheduler(quantum=-1)
    
    def test_rr_procesos_vacios(self):
        """Test: RR con lista vacía retorna lista vacía."""
        scheduler = RoundRobinScheduler(quantum=4)
        gantt = scheduler.planificar([])
        assert gantt == []
    
    def test_rr_un_proceso(self):
        """Test: RR con un solo proceso que cabe en un quantum."""
        scheduler = RoundRobinScheduler(quantum=10)
        proceso = Proceso("P1", 5, 1)
        gantt = scheduler.planificar([proceso])
        
        assert len(gantt) == 1
        assert gantt[0] == ("P1", 0, 5)
    
    def test_rr_un_proceso_multiple_quantums(self):
        """Test: RR con un proceso que requiere múltiples quantums."""
        scheduler = RoundRobinScheduler(quantum=3)
        proceso = Proceso("P1", 10, 1)
        gantt = scheduler.planificar([proceso])
        
        # 10 unidades con quantum 3: necesita 4 ciclos (3+3+3+1)
        assert len(gantt) == 4
        assert gantt[0] == ("P1", 0, 3)
        assert gantt[1] == ("P1", 3, 6)
        assert gantt[2] == ("P1", 6, 9)
        assert gantt[3] == ("P1", 9, 10)
    
    def test_rr_multiples_procesos(self):
        """Test: RR con múltiples procesos alterna entre ellos."""
        scheduler = RoundRobinScheduler(quantum=4)
        procesos = [
            Proceso("P1", 10, 1),
            Proceso("P2", 5, 2),
            Proceso("P3", 2, 1)
        ]
        
        gantt = scheduler.planificar(procesos)
        
        # Verificar que hay múltiples entradas y que los PIDs se alternan
        assert len(gantt) > 3
        
        # P3 debería terminar primero (2 unidades < quantum)
        # Verificar que los procesos se ejecutan en ciclos
        pids = [entrada[0] for entrada in gantt]
        assert pids[0] == "P1"  # Primera ronda: P1
        assert pids[1] == "P2"  # Primera ronda: P2
        assert pids[2] == "P3"  # Primera ronda: P3 (termina)
    
    def test_rr_quantum_mayor_que_duracion(self):
        """Test: RR con quantum mayor que todas las duraciones actúa como FCFS."""
        scheduler = RoundRobinScheduler(quantum=20)
        procesos = [
            Proceso("P1", 5, 1),
            Proceso("P2", 3, 2),
            Proceso("P3", 8, 1)
        ]
        
        gantt = scheduler.planificar(procesos)
        
        # Cada proceso se ejecuta completo en su turno
        assert len(gantt) == 3
        assert gantt[0] == ("P1", 0, 5)
        assert gantt[1] == ("P2", 5, 8)
        assert gantt[2] == ("P3", 8, 16)
    
    def test_rr_actualiza_tiempos_procesos(self):
        """Test: RR actualiza tiempo_inicio y tiempo_fin."""
        scheduler = RoundRobinScheduler(quantum=4)
        procesos = [
            Proceso("P1", 5, 1),
            Proceso("P2", 3, 2)
        ]
        
        scheduler.planificar(procesos)
        
        assert procesos[0].tiempo_inicio is not None
        assert procesos[0].tiempo_fin is not None
        assert procesos[1].tiempo_inicio is not None
        assert procesos[1].tiempo_fin is not None
        assert procesos[0].tiempo_restante == 0
        assert procesos[1].tiempo_restante == 0
    
    def test_rr_tiempo_total_correcto(self):
        """Test: RR calcula el tiempo total de ejecución correctamente."""
        scheduler = RoundRobinScheduler(quantum=2)
        procesos = [
            Proceso("P1", 4, 1),
            Proceso("P2", 3, 2)
        ]
        
        gantt = scheduler.planificar(procesos)
        
        # Tiempo total debe ser 4 + 3 = 7
        tiempo_final = gantt[-1][2]
        assert tiempo_final == 7
