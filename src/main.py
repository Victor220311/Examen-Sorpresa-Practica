"""
Programa principal con interfaz de línea de comandos para el sistema de planificación.
Permite gestionar procesos, ejecutar simulaciones y mostrar resultados.
"""

import sys
import os
from proceso import Proceso
from scheduler import FCFSScheduler, RoundRobinScheduler
from repositorio import RepositorioProcesos
from metrics import MetricasCalculator


class SistemaPlanificacion:
    """
    Sistema principal que gestiona la interfaz de usuario y coordina los componentes.
    """
    
    def __init__(self):
        """Inicializa el sistema con un repositorio vacío."""
        self.repositorio = RepositorioProcesos()
        self.scheduler_fcfs = FCFSScheduler()
        self.scheduler_rr = None  # Se creará cuando se especifique el quantum
    
    def mostrar_menu(self):
        """Muestra el menú principal de opciones."""
        print("\n" + "="*80)
        print("SISTEMA DE PLANIFICACIÓN DE PROCESOS")
        print("="*80)
        print("1. Agregar proceso")
        print("2. Listar procesos")
        print("3. Eliminar proceso")
        print("4. Ejecutar simulación FCFS")
        print("5. Ejecutar simulación Round-Robin")
        print("6. Guardar procesos (JSON)")
        print("7. Cargar procesos (JSON)")
        print("8. Guardar procesos (CSV)")
        print("9. Cargar procesos (CSV)")
        print("10. Limpiar todos los procesos")
        print("0. Salir")
        print("="*80)
    
    def agregar_proceso(self):
        """Solicita datos al usuario y agrega un nuevo proceso."""
        print("\n--- AGREGAR PROCESO ---")
        try:
            pid = input("Ingrese el PID del proceso: ").strip()
            duracion = int(input("Ingrese la duración (tiempo de CPU): "))
            prioridad = int(input("Ingrese la prioridad (menor = más urgente): "))
            tiempo_llegada = int(input("Ingrese el tiempo de llegada (por defecto 0): ") or "0")
            
            proceso = Proceso(pid, duracion, prioridad, tiempo_llegada)
            
            if self.repositorio.agregar_proceso(proceso):
                print(f"✓ Proceso '{pid}' agregado exitosamente.")
            else:
                print(f"✗ Error: Ya existe un proceso con PID '{pid}'.")
        
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Error inesperado: {e}")
    
    def listar_procesos(self):
        """Lista todos los procesos registrados."""
        print("\n--- LISTA DE PROCESOS ---")
        procesos = self.repositorio.listar_procesos()
        
        if not procesos:
            print("No hay procesos registrados.")
            return
        
        print(f"\nTotal de procesos: {len(procesos)}")
        print("-" * 80)
        print(f"{'PID':<15} {'Duración':<15} {'Prioridad':<15} {'Tiempo Llegada':<15}")
        print("-" * 80)
        
        for proceso in procesos:
            print(f"{proceso.pid:<15} {proceso.duracion:<15} "
                  f"{proceso.prioridad:<15} {proceso.tiempo_llegada:<15}")
    
    def eliminar_proceso(self):
        """Solicita un PID y elimina el proceso correspondiente."""
        print("\n--- ELIMINAR PROCESO ---")
        pid = input("Ingrese el PID del proceso a eliminar: ").strip()
        
        if self.repositorio.eliminar_proceso(pid):
            print(f"✓ Proceso '{pid}' eliminado exitosamente.")
        else:
            print(f"✗ Error: No existe un proceso con PID '{pid}'.")
    
    def ejecutar_fcfs(self):
        """Ejecuta una simulación con el algoritmo FCFS."""
        print("\n--- SIMULACIÓN FCFS (First-Come, First-Served) ---")
        
        procesos = self.repositorio.listar_procesos()
        if not procesos:
            print("✗ No hay procesos para planificar.")
            return
        
        # Reiniciar procesos antes de planificar
        for p in procesos:
            p.reiniciar()
        
        # Ejecutar planificación
        gantt = self.scheduler_fcfs.planificar(procesos)
        
        # Mostrar diagrama de Gantt
        print(MetricasCalculator.mostrar_gantt(gantt))
        print(MetricasCalculator.crear_grafico_gantt_texto(gantt))
        
        # Calcular y mostrar métricas
        metricas = MetricasCalculator.calcular_metricas(procesos, gantt)
        print(MetricasCalculator.mostrar_metricas(metricas))
    
    def ejecutar_round_robin(self):
        """Ejecuta una simulación con el algoritmo Round-Robin."""
        print("\n--- SIMULACIÓN ROUND-ROBIN ---")
        
        procesos = self.repositorio.listar_procesos()
        if not procesos:
            print("✗ No hay procesos para planificar.")
            return
        
        try:
            quantum = int(input("Ingrese el quantum (tiempo por ciclo): "))
            
            if quantum <= 0:
                print("✗ El quantum debe ser un entero positivo.")
                return
            
            # Crear scheduler con el quantum especificado
            scheduler_rr = RoundRobinScheduler(quantum)
            
            # Reiniciar procesos antes de planificar
            for p in procesos:
                p.reiniciar()
            
            # Ejecutar planificación
            gantt = scheduler_rr.planificar(procesos)
            
            # Mostrar diagrama de Gantt
            print(MetricasCalculator.mostrar_gantt(gantt))
            print(MetricasCalculator.crear_grafico_gantt_texto(gantt))
            
            # Calcular y mostrar métricas
            metricas = MetricasCalculator.calcular_metricas(procesos, gantt)
            print(MetricasCalculator.mostrar_metricas(metricas))
        
        except ValueError as e:
            print(f"✗ Error: {e}")
    
    def guardar_json(self):
        """Guarda los procesos en un archivo JSON."""
        print("\n--- GUARDAR PROCESOS (JSON) ---")
        ruta = input("Ingrese la ruta del archivo (por defecto 'procesos.json'): ").strip()
        if not ruta:
            ruta = "procesos.json"
        
        try:
            self.repositorio.guardar_json(ruta)
            print(f"✓ Procesos guardados exitosamente en '{ruta}'.")
        except Exception as e:
            print(f"✗ Error al guardar: {e}")
    
    def cargar_json(self):
        """Carga procesos desde un archivo JSON."""
        print("\n--- CARGAR PROCESOS (JSON) ---")
        ruta = input("Ingrese la ruta del archivo: ").strip()
        
        try:
            self.repositorio.cargar_json(ruta)
            print(f"✓ Procesos cargados exitosamente desde '{ruta}'.")
            print(f"Total de procesos: {self.repositorio.cantidad_procesos()}")
        except Exception as e:
            print(f"✗ Error al cargar: {e}")
    
    def guardar_csv(self):
        """Guarda los procesos en un archivo CSV."""
        print("\n--- GUARDAR PROCESOS (CSV) ---")
        ruta = input("Ingrese la ruta del archivo (por defecto 'procesos.csv'): ").strip()
        if not ruta:
            ruta = "procesos.csv"
        
        try:
            self.repositorio.guardar_csv(ruta)
            print(f"✓ Procesos guardados exitosamente en '{ruta}'.")
        except Exception as e:
            print(f"✗ Error al guardar: {e}")
    
    def cargar_csv(self):
        """Carga procesos desde un archivo CSV."""
        print("\n--- CARGAR PROCESOS (CSV) ---")
        ruta = input("Ingrese la ruta del archivo: ").strip()
        
        try:
            self.repositorio.cargar_csv(ruta)
            print(f"✓ Procesos cargados exitosamente desde '{ruta}'.")
            print(f"Total de procesos: {self.repositorio.cantidad_procesos()}")
        except Exception as e:
            print(f"✗ Error al cargar: {e}")
    
    def limpiar_procesos(self):
        """Elimina todos los procesos del repositorio."""
        print("\n--- LIMPIAR PROCESOS ---")
        confirmacion = input("¿Está seguro de eliminar todos los procesos? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            self.repositorio.limpiar()
            print("✓ Todos los procesos han sido eliminados.")
        else:
            print("Operación cancelada.")
    
    def ejecutar(self):
        """Bucle principal del programa."""
        print("\n¡Bienvenido al Sistema de Planificación de Procesos!")
        
        while True:
            self.mostrar_menu()
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.agregar_proceso()
            elif opcion == "2":
                self.listar_procesos()
            elif opcion == "3":
                self.eliminar_proceso()
            elif opcion == "4":
                self.ejecutar_fcfs()
            elif opcion == "5":
                self.ejecutar_round_robin()
            elif opcion == "6":
                self.guardar_json()
            elif opcion == "7":
                self.cargar_json()
            elif opcion == "8":
                self.guardar_csv()
            elif opcion == "9":
                self.cargar_csv()
            elif opcion == "10":
                self.limpiar_procesos()
            elif opcion == "0":
                print("\n¡Gracias por usar el Sistema de Planificación de Procesos!")
                print("Hasta luego.\n")
                break
            else:
                print("\n✗ Opción no válida. Por favor, intente nuevamente.")
            
            input("\nPresione Enter para continuar...")


def main():
    """Función principal que inicia el sistema."""
    sistema = SistemaPlanificacion()
    sistema.ejecutar()


if __name__ == "__main__":
    main()
