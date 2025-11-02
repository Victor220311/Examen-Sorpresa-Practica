"""
Módulo que define la clase Proceso para representar procesos del sistema.
Un proceso tiene un PID único, duración de CPU y prioridad.
"""


class Proceso:
    """
    Representa un proceso del sistema operativo con sus atributos básicos.
    
    Atributos:
        pid (str): Identificador único del proceso
        duracion (int): Tiempo total de CPU requerido (en unidades de tiempo)
        prioridad (int): Prioridad del proceso (menor valor = mayor prioridad)
        tiempo_restante (int): Tiempo de CPU que aún falta por ejecutar
        tiempo_llegada (int): Momento en que el proceso llega al sistema (por defecto 0)
        tiempo_inicio (int): Momento en que el proceso inicia su primera ejecución
        tiempo_fin (int): Momento en que el proceso finaliza completamente
    """
    
    def __init__(self, pid: str, duracion: int, prioridad: int, tiempo_llegada: int = 0):
        """
        Inicializa un nuevo proceso con validación de parámetros.
        
        Args:
            pid (str): Identificador único del proceso (no vacío)
            duracion (int): Duración total de CPU requerida (debe ser positivo)
            prioridad (int): Nivel de prioridad del proceso
            tiempo_llegada (int): Tiempo de llegada del proceso (por defecto 0)
        
        Raises:
            ValueError: Si el PID está vacío o la duración no es positiva
        """
        if not pid or not isinstance(pid, str) or pid.strip() == "": #Si pid es un str o no hay nada
            raise ValueError("El PID no puede estar vacío")
        
        if not isinstance(duracion, int) or duracion <= 0:
            raise ValueError("La duración debe ser un entero positivo")
        
        if not isinstance(prioridad, int):
            raise ValueError("La prioridad debe ser un entero")
        
        if not isinstance(tiempo_llegada, int) or tiempo_llegada < 0:
            raise ValueError("El tiempo de llegada debe ser un entero no negativo")
        
        self.pid = pid
        self.duracion = duracion
        self.prioridad = prioridad
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_restante = duracion  # Inicialmente igual a la duración total
        self.tiempo_inicio = None  # Se establece durante la planificación
        self.tiempo_fin = None  # Se establece durante la planificación
    
    def __repr__(self):
        """Representación en string del proceso para debugging."""
        return (f"Proceso(pid='{self.pid}', duracion={self.duracion}, "
                f"prioridad={self.prioridad}, tiempo_restante={self.tiempo_restante})")
    
    def __str__(self):
        """Representación legible del proceso para el usuario."""
        return (f"PID: {self.pid}, Duración: {self.duracion}, "
                f"Prioridad: {self.prioridad}, Tiempo restante: {self.tiempo_restante}")
    
    def reiniciar(self):
        """Reinicia el proceso a su estado inicial para una nueva simulación."""
        self.tiempo_restante = self.duracion
        self.tiempo_inicio = None
        self.tiempo_fin = None
    
    def to_dict(self):
        """
        Convierte el proceso a un diccionario para serialización.
        
        Returns:
            dict: Diccionario con los atributos del proceso
        """
        return {
            'pid': self.pid,
            'duracion': self.duracion,
            'prioridad': self.prioridad,
            'tiempo_llegada': self.tiempo_llegada
        }
    
    @classmethod #Crear un proceso a partir de un diccionario (csv, json)
    def from_dict(cls, data: dict):
        """
        Crea un proceso a partir de un diccionario.
        
        Args:
            data (dict): Diccionario con los atributos del proceso
        
        Returns:
            Proceso: Nueva instancia de Proceso
        """
        return cls(
            pid=data['pid'],
            duracion=int(data['duracion']),
            prioridad=int(data['prioridad']),
            tiempo_llegada=int(data.get('tiempo_llegada', 0))
        )
