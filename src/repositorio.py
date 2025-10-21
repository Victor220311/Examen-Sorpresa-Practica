"""
Módulo que gestiona el repositorio de procesos y la persistencia de datos.
Permite agregar, listar, eliminar procesos y guardar/cargar desde archivos CSV y JSON.
"""

import json
import csv
from typing import List, Optional
from proceso import Proceso


class RepositorioProcesos:
    """
    Gestiona el conjunto de procesos activos y su persistencia en disco.
    """
    
    def __init__(self):
        """Inicializa un repositorio vacío de procesos."""
        self._procesos = {}  # Diccionario con PID como clave
    
    def agregar_proceso(self, proceso: Proceso) -> bool:
        """
        Agrega un proceso al repositorio.
        
        Args:
            proceso (Proceso): Proceso a agregar
        
        Returns:
            bool: True si se agregó correctamente, False si el PID ya existe
        
        Raises:
            ValueError: Si el proceso no es una instancia válida
        """
        if not isinstance(proceso, Proceso):
            raise ValueError("El objeto debe ser una instancia de Proceso")
        
        if proceso.pid in self._procesos:
            return False  # PID duplicado
        
        self._procesos[proceso.pid] = proceso
        return True
    
    def eliminar_proceso(self, pid: str) -> bool:
        """
        Elimina un proceso del repositorio por su PID.
        
        Args:
            pid (str): Identificador del proceso a eliminar
        
        Returns:
            bool: True si se eliminó, False si no existe
        """
        if pid in self._procesos:
            del self._procesos[pid]
            return True
        return False
    
    def obtener_proceso(self, pid: str) -> Optional[Proceso]:
        """
        Obtiene un proceso por su PID.
        
        Args:
            pid (str): Identificador del proceso
        
        Returns:
            Optional[Proceso]: El proceso si existe, None en caso contrario
        """
        return self._procesos.get(pid)
    
    def listar_procesos(self) -> List[Proceso]:
        """
        Lista todos los procesos registrados.
        
        Returns:
            List[Proceso]: Lista con todos los procesos
        """
        return list(self._procesos.values())
    
    def cantidad_procesos(self) -> int:
        """
        Retorna la cantidad de procesos en el repositorio.
        
        Returns:
            int: Número de procesos
        """
        return len(self._procesos)
    
    def limpiar(self):
        """Elimina todos los procesos del repositorio."""
        self._procesos.clear()
    
    def guardar_json(self, ruta_archivo: str):
        """
        Guarda todos los procesos en un archivo JSON.
        
        Args:
            ruta_archivo (str): Ruta del archivo donde guardar
        
        Raises:
            IOError: Si hay problemas al escribir el archivo
        """
        try:
            procesos_lista = [p.to_dict() for p in self._procesos.values()]
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(procesos_lista, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise IOError(f"Error al guardar el archivo JSON: {e}")
    
    def cargar_json(self, ruta_archivo: str):
        """
        Carga procesos desde un archivo JSON, reemplazando los existentes.
        
        Args:
            ruta_archivo (str): Ruta del archivo a cargar
        
        Raises:
            IOError: Si hay problemas al leer el archivo
            ValueError: Si el formato del archivo es inválido
        """
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                procesos_lista = json.load(f)
            
            # Limpiar procesos actuales
            self._procesos.clear()
            
            # Cargar nuevos procesos
            for datos in procesos_lista:
                proceso = Proceso.from_dict(datos)
                self._procesos[proceso.pid] = proceso
                
        except FileNotFoundError:
            raise IOError(f"Archivo no encontrado: {ruta_archivo}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error al decodificar JSON: {e}")
        except Exception as e:
            raise IOError(f"Error al cargar el archivo JSON: {e}")
    
    def guardar_csv(self, ruta_archivo: str):
        """
        Guarda todos los procesos en un archivo CSV con separador ';'.
        
        Args:
            ruta_archivo (str): Ruta del archivo donde guardar
        
        Raises:
            IOError: Si hay problemas al escribir el archivo
        """
        try:
            with open(ruta_archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                # Escribir encabezado
                writer.writerow(['pid', 'duracion', 'prioridad', 'tiempo_llegada'])
                # Escribir datos de cada proceso
                for proceso in self._procesos.values():
                    writer.writerow([
                        proceso.pid,
                        proceso.duracion,
                        proceso.prioridad,
                        proceso.tiempo_llegada
                    ])
        except Exception as e:
            raise IOError(f"Error al guardar el archivo CSV: {e}")
    
    def cargar_csv(self, ruta_archivo: str):
        """
        Carga procesos desde un archivo CSV, reemplazando los existentes.
        
        Args:
            ruta_archivo (str): Ruta del archivo a cargar
        
        Raises:
            IOError: Si hay problemas al leer el archivo
            ValueError: Si el formato del archivo es inválido
        """
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                
                # Limpiar procesos actuales
                self._procesos.clear()
                
                # Cargar nuevos procesos
                for fila in reader:
                    proceso = Proceso(
                        pid=fila['pid'],
                        duracion=int(fila['duracion']),
                        prioridad=int(fila['prioridad']),
                        tiempo_llegada=int(fila.get('tiempo_llegada', 0))
                    )
                    self._procesos[proceso.pid] = proceso
                    
        except FileNotFoundError:
            raise IOError(f"Archivo no encontrado: {ruta_archivo}")
        except KeyError as e:
            raise ValueError(f"Falta columna requerida en CSV: {e}")
        except ValueError as e:
            raise ValueError(f"Error en formato de datos CSV: {e}")
        except Exception as e:
            raise IOError(f"Error al cargar el archivo CSV: {e}")
    
    def __len__(self):
        """Permite usar len() sobre el repositorio."""
        return len(self._procesos)
    
    def __repr__(self):
        """Representación del repositorio."""
        return f"RepositorioProcesos(cantidad={len(self._procesos)})"
