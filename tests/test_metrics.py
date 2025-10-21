"""
Pruebas unitarias para el cálculo de métricas.
"""

import pytest
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from proceso import Proceso
from scheduler import FCFSScheduler, RoundRobinScheduler, GanttEntry
from metrics import MetricasCalculator


class TestMetricasCalculator:
    """Tests para el cálculo de métricas."""
    
    def test_metricas_listas_vacias(self):
        """Test: Métricas con listas vacías retorna valores en 0."""
        metricas = MetricasCalculator.calcular_metricas([], [])
        
        assert metricas['tiempo_respuesta_promedio'] == 0
        assert metricas['tiempo_espera_promedio'] == 0
        assert metricas['tiempo_retorno_promedio'] == 0
        assert len(metricas['metricas_individuales']) == 0
    
    def test_metricas_un_proceso_simple(self):
        """Test: Métricas para un proceso que inicia en t=0."""
        proceso = Proceso("P1", 10, 1)
        gantt = [("P1", 0, 10)]
        
        metricas = MetricasCalculator.calcular_metricas([proceso], gantt)
        
        # Tiempo de respuesta = 0 - 0 = 0
        # Tiempo de retorno = 10 - 0 = 10
        # Tiempo de espera = 10 - 10 = 0
        assert metricas['metricas_individuales']['P1']['tiempo_respuesta'] == 0
        assert metricas['metricas_individuales']['P1']['tiempo_retorno'] == 10
        assert metricas['metricas_individuales']['P1']['tiempo_espera'] == 0
    
    def test_metricas_proceso_con_espera(self):
        """Test: Métricas para proceso que espera antes de ejecutar."""
        proceso = Proceso("P1", 5, 1)
        # El proceso espera hasta t=3, luego se ejecuta de 3 a 8
        gantt = [("P1", 3, 8)]
        
        metricas = MetricasCalculator.calcular_metricas([proceso], gantt)
        
        # Tiempo de respuesta = 3 - 0 = 3
        # Tiempo de retorno = 8 - 0 = 8
        # Tiempo de espera = 8 - 5 = 3
        assert metricas['metricas_individuales']['P1']['tiempo_respuesta'] == 3
        assert metricas['metricas_individuales']['P1']['tiempo_retorno'] == 8
        assert metricas['metricas_individuales']['P1']['tiempo_espera'] == 3
    
    def test_metricas_multiples_procesos_fcfs(self):
        """Test: Métricas para múltiples procesos con FCFS."""
        procesos = [
            Proceso("P1", 5, 1),
            Proceso("P2", 3, 2),
            Proceso("P3", 2, 1)
        ]
        
        # Simular FCFS
        scheduler = FCFSScheduler()
        gantt = scheduler.planificar(procesos)
        
        metricas = MetricasCalculator.calcular_metricas(procesos, gantt)
        
        # P1: respuesta=0, retorno=5, espera=0
        # P2: respuesta=5, retorno=8, espera=5
        # P3: respuesta=8, retorno=10, espera=8
        assert metricas['metricas_individuales']['P1']['tiempo_respuesta'] == 0
        assert metricas['metricas_individuales']['P2']['tiempo_respuesta'] == 5
        assert metricas['metricas_individuales']['P3']['tiempo_respuesta'] == 8
        
        # Promedios
        # Respuesta promedio = (0 + 5 + 8) / 3 = 4.33...
        # Espera promedio = (0 + 5 + 8) / 3 = 4.33...
        # Retorno promedio = (5 + 8 + 10) / 3 = 7.66...
        assert abs(metricas['tiempo_respuesta_promedio'] - 4.333) < 0.01
        assert abs(metricas['tiempo_espera_promedio'] - 4.333) < 0.01
        assert abs(metricas['tiempo_retorno_promedio'] - 7.666) < 0.01
    
    def test_metricas_round_robin(self):
        """Test: Métricas para Round-Robin con múltiples ciclos."""
        procesos = [
            Proceso("P1", 6, 1),
            Proceso("P2", 4, 2)
        ]
        
        # Simular Round-Robin con quantum 2
        scheduler = RoundRobinScheduler(quantum=2)
        gantt = scheduler.planificar(procesos)
        
        metricas = MetricasCalculator.calcular_metricas(procesos, gantt)
        
        # Verificar que se calcularon métricas para ambos procesos
        assert 'P1' in metricas['metricas_individuales']
        assert 'P2' in metricas['metricas_individuales']
        
        # P1 inicia en 0
        assert metricas['metricas_individuales']['P1']['tiempo_respuesta'] == 0
        
        # P2 inicia en 2 (después del primer quantum de P1)
        assert metricas['metricas_individuales']['P2']['tiempo_respuesta'] == 2
    
    def test_metricas_proceso_interrumpido(self):
        """Test: Métricas con proceso que se ejecuta en múltiples segmentos."""
        proceso = Proceso("P1", 6, 1)
        # P1 se ejecuta en tres segmentos
        gantt = [
            ("P1", 0, 2),
            ("P1", 4, 6),
            ("P1", 8, 10)
        ]
        
        metricas = MetricasCalculator.calcular_metricas([proceso], gantt)
        
        # Tiempo de respuesta = primer inicio - llegada = 0 - 0 = 0
        # Tiempo de retorno = último fin - llegada = 10 - 0 = 10
        # Tiempo de espera = retorno - duración = 10 - 6 = 4
        assert metricas['metricas_individuales']['P1']['tiempo_respuesta'] == 0
        assert metricas['metricas_individuales']['P1']['tiempo_retorno'] == 10
        assert metricas['metricas_individuales']['P1']['tiempo_espera'] == 4
    
    def test_mostrar_metricas_formato(self):
        """Test: Formato de salida de métricas."""
        procesos = [Proceso("P1", 5, 1)]
        gantt = [("P1", 0, 5)]
        
        metricas = MetricasCalculator.calcular_metricas(procesos, gantt)
        salida = MetricasCalculator.mostrar_metricas(metricas)
        
        # Verificar que la salida contiene elementos clave
        assert "MÉTRICAS DE RENDIMIENTO" in salida
        assert "P1" in salida
        assert "PROMEDIOS" in salida
    
    def test_mostrar_gantt_formato(self):
        """Test: Formato de salida del diagrama de Gantt."""
        gantt = [
            ("P1", 0, 5),
            ("P2", 5, 8),
            ("P3", 8, 10)
        ]
        
        salida = MetricasCalculator.mostrar_gantt(gantt)
        
        assert "DIAGRAMA DE GANTT" in salida
        assert "P1" in salida
        assert "P2" in salida
        assert "P3" in salida
    
    def test_mostrar_gantt_vacio(self):
        """Test: Mostrar Gantt vacío."""
        salida = MetricasCalculator.mostrar_gantt([])
        
        assert "No hay ejecuciones" in salida
    
    def test_grafico_gantt_texto(self):
        """Test: Crear representación visual del Gantt."""
        gantt = [
            ("P1", 0, 3),
            ("P2", 3, 5)
        ]
        
        salida = MetricasCalculator.crear_grafico_gantt_texto(gantt)
        
        assert "P1" in salida
        assert "P2" in salida
        assert "█" in salida  # Debe contener la barra visual
    
    def test_metricas_con_tiempo_llegada_diferente(self):
        """Test: Métricas con procesos que llegan en diferentes tiempos."""
        procesos = [
            Proceso("P1", 3, 1, tiempo_llegada=0),
            Proceso("P2", 2, 2, tiempo_llegada=2)
        ]
        
        # P1 ejecuta de 0-3, P2 de 3-5
        gantt = [
            ("P1", 0, 3),
            ("P2", 3, 5)
        ]
        
        metricas = MetricasCalculator.calcular_metricas(procesos, gantt)
        
        # P1: respuesta = 0-0 = 0
        # P2: respuesta = 3-2 = 1
        assert metricas['metricas_individuales']['P1']['tiempo_respuesta'] == 0
        assert metricas['metricas_individuales']['P2']['tiempo_respuesta'] == 1
        
        # P1: retorno = 3-0 = 3
        # P2: retorno = 5-2 = 3
        assert metricas['metricas_individuales']['P1']['tiempo_retorno'] == 3
        assert metricas['metricas_individuales']['P2']['tiempo_retorno'] == 3
