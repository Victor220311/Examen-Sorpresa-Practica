"""
Módulo para el cálculo de métricas de rendimiento de los procesos planificados.
Incluye tiempos de respuesta, espera y retorno.
"""

from typing import List, Dict, Tuple
from proceso import Proceso
from scheduler import GanttEntry


class MetricasCalculator:
    """
    Calcula métricas de rendimiento a partir del diagrama de Gantt y los procesos.
    """
    
    @staticmethod
    def calcular_metricas(procesos: List[Proceso], gantt: List[GanttEntry]) -> Dict[str, any]:
        """
        Calcula todas las métricas de rendimiento para un conjunto de procesos planificados.
        
        Métricas calculadas:
        - Tiempo de respuesta: tiempo desde llegada hasta primera ejecución
        - Tiempo de retorno (turnaround): tiempo desde llegada hasta finalización
        - Tiempo de espera: tiempo total esperando en cola (retorno - duración)
        
        Args:
            procesos (List[Proceso]): Lista de procesos planificados
            gantt (List[GanttEntry]): Diagrama de Gantt con las ejecuciones
        
        Returns:
            Dict: Diccionario con métricas individuales y promedios
        """
        if not procesos or not gantt:
            return {
                'metricas_individuales': {},
                'tiempo_respuesta_promedio': 0,
                'tiempo_espera_promedio': 0,
                'tiempo_retorno_promedio': 0
            }
        
        # Encontrar el primer inicio y último fin de cada proceso en el Gantt
        primer_inicio = {}  # PID -> primer tiempo de inicio
        ultimo_fin = {}     # PID -> último tiempo de fin
        
        for pid, inicio, fin in gantt:
            if pid not in primer_inicio:
                primer_inicio[pid] = inicio
            ultimo_fin[pid] = fin
        
        # Calcular métricas individuales
        metricas_individuales = {}
        tiempos_respuesta = []
        tiempos_espera = []
        tiempos_retorno = []
        
        for proceso in procesos:
            pid = proceso.pid
            
            if pid not in primer_inicio or pid not in ultimo_fin:
                continue
            
            # Tiempo de respuesta = primer_inicio - tiempo_llegada
            tiempo_respuesta = primer_inicio[pid] - proceso.tiempo_llegada
            
            # Tiempo de retorno = ultimo_fin - tiempo_llegada
            tiempo_retorno = ultimo_fin[pid] - proceso.tiempo_llegada
            
            # Tiempo de espera = tiempo_retorno - duración
            tiempo_espera = tiempo_retorno - proceso.duracion
            
            metricas_individuales[pid] = {
                'tiempo_respuesta': tiempo_respuesta,
                'tiempo_espera': tiempo_espera,
                'tiempo_retorno': tiempo_retorno,
                'duracion': proceso.duracion,
                'tiempo_llegada': proceso.tiempo_llegada
            }
            
            tiempos_respuesta.append(tiempo_respuesta)
            tiempos_espera.append(tiempo_espera)
            tiempos_retorno.append(tiempo_retorno)
        
        # Calcular promedios
        n = len(tiempos_respuesta)
        tiempo_respuesta_promedio = sum(tiempos_respuesta) / n if n > 0 else 0
        tiempo_espera_promedio = sum(tiempos_espera) / n if n > 0 else 0
        tiempo_retorno_promedio = sum(tiempos_retorno) / n if n > 0 else 0
        
        return {
            'metricas_individuales': metricas_individuales,
            'tiempo_respuesta_promedio': tiempo_respuesta_promedio,
            'tiempo_espera_promedio': tiempo_espera_promedio,
            'tiempo_retorno_promedio': tiempo_retorno_promedio
        }
    
    @staticmethod
    def mostrar_metricas(metricas: Dict[str, any]) -> str:
        """
        Formatea las métricas en un string legible para mostrar al usuario.
        
        Args:
            metricas (Dict): Diccionario con las métricas calculadas
        
        Returns:
            str: String formateado con las métricas
        """
        resultado = []
        resultado.append("\n" + "="*80)
        resultado.append("MÉTRICAS DE RENDIMIENTO")
        resultado.append("="*80)
        
        # Métricas individuales
        resultado.append("\nMétricas individuales por proceso:")
        resultado.append("-" * 80)
        resultado.append(f"{'PID':<10} {'Duración':<10} {'T.Respuesta':<15} {'T.Espera':<15} {'T.Retorno':<15}")
        resultado.append("-" * 80)
        
        for pid, datos in metricas['metricas_individuales'].items():
            resultado.append(
                f"{pid:<10} "
                f"{datos['duracion']:<10} "
                f"{datos['tiempo_respuesta']:<15.2f} "
                f"{datos['tiempo_espera']:<15.2f} "
                f"{datos['tiempo_retorno']:<15.2f}"
            )
        
        # Promedios
        resultado.append("\n" + "="*80)
        resultado.append("PROMEDIOS")
        resultado.append("="*80)
        resultado.append(f"Tiempo de respuesta promedio: {metricas['tiempo_respuesta_promedio']:.2f} unidades")
        resultado.append(f"Tiempo de espera promedio:    {metricas['tiempo_espera_promedio']:.2f} unidades")
        resultado.append(f"Tiempo de retorno promedio:   {metricas['tiempo_retorno_promedio']:.2f} unidades")
        resultado.append("="*80 + "\n")
        
        return "\n".join(resultado)
    
    @staticmethod
    def mostrar_gantt(gantt: List[GanttEntry]) -> str:
        """
        Formatea el diagrama de Gantt en un string legible.
        
        Args:
            gantt (List[GanttEntry]): Diagrama de Gantt
        
        Returns:
            str: String formateado con el diagrama de Gantt
        """
        if not gantt:
            return "No hay ejecuciones en el diagrama de Gantt"
        
        resultado = []
        resultado.append("\n" + "="*80)
        resultado.append("DIAGRAMA DE GANTT")
        resultado.append("="*80)
        resultado.append(f"{'PID':<15} {'Tiempo Inicio':<20} {'Tiempo Fin':<20} {'Duración':<15}")
        resultado.append("-" * 80)
        
        for pid, inicio, fin in gantt:
            duracion = fin - inicio
            resultado.append(f"{pid:<15} {inicio:<20} {fin:<20} {duracion:<15}")
        
        resultado.append("="*80 + "\n")
        
        return "\n".join(resultado)
    
    @staticmethod
    def crear_grafico_gantt_texto(gantt: List[GanttEntry]) -> str:
        """
        Crea una representación visual simple del diagrama de Gantt usando caracteres.
        
        Args:
            gantt (List[GanttEntry]): Diagrama de Gantt
        
        Returns:
            str: Representación visual del Gantt
        """
        if not gantt:
            return "No hay ejecuciones para mostrar"
        
        resultado = []
        resultado.append("\nRepresentación visual del Gantt:")
        resultado.append("-" * 80)
        
        # Encontrar el tiempo máximo
        tiempo_max = max(fin for _, _, fin in gantt)
        
        # Crear la línea de tiempo
        for pid, inicio, fin in gantt:
            duracion = fin - inicio
            # Crear la barra visual
            espacios_antes = ' ' * (inicio * 2)
            barra = '█' * (duracion * 2)
            linea = f"{pid:<10} |{espacios_antes}{barra}"
            resultado.append(linea)
        
        # Agregar escala de tiempo
        resultado.append(" " * 11 + "|" + "-" * (tiempo_max * 2))
        escala = " " * 11 + "|"
        for i in range(0, tiempo_max + 1, max(1, tiempo_max // 10)):
            pos = i * 2
            escala = escala[:11 + pos] + str(i) + escala[11 + pos + len(str(i)):]
        resultado.append(escala)
        
        return "\n".join(resultado)
