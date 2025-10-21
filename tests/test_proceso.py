"""
Pruebas unitarias para la clase Proceso.
"""

import pytest
import sys
import os

# Agregar el directorio src al path para poder importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from proceso import Proceso


class TestProceso:
    """Tests para la clase Proceso."""
    
    def test_crear_proceso_valido(self):
        """Test: Crear un proceso con parámetros válidos."""
        proceso = Proceso("P1", 10, 1)
        assert proceso.pid == "P1"
        assert proceso.duracion == 10
        assert proceso.prioridad == 1
        assert proceso.tiempo_llegada == 0
        assert proceso.tiempo_restante == 10
    
    def test_crear_proceso_con_tiempo_llegada(self):
        """Test: Crear un proceso con tiempo de llegada personalizado."""
        proceso = Proceso("P2", 5, 2, tiempo_llegada=3)
        assert proceso.tiempo_llegada == 3
        assert proceso.tiempo_restante == 5
    
    def test_pid_vacio_lanza_error(self):
        """Test: PID vacío debe lanzar ValueError."""
        with pytest.raises(ValueError, match="El PID no puede estar vacío"):
            Proceso("", 10, 1)
    
    def test_pid_solo_espacios_lanza_error(self):
        """Test: PID con solo espacios debe lanzar ValueError."""
        with pytest.raises(ValueError, match="El PID no puede estar vacío"):
            Proceso("   ", 10, 1)
    
    def test_duracion_negativa_lanza_error(self):
        """Test: Duración negativa debe lanzar ValueError."""
        with pytest.raises(ValueError, match="La duración debe ser un entero positivo"):
            Proceso("P1", -5, 1)
    
    def test_duracion_cero_lanza_error(self):
        """Test: Duración cero debe lanzar ValueError."""
        with pytest.raises(ValueError, match="La duración debe ser un entero positivo"):
            Proceso("P1", 0, 1)
    
    def test_prioridad_debe_ser_entero(self):
        """Test: Prioridad debe ser un entero."""
        with pytest.raises(ValueError, match="La prioridad debe ser un entero"):
            Proceso("P1", 10, "alta")
    
    def test_tiempo_llegada_negativo_lanza_error(self):
        """Test: Tiempo de llegada negativo debe lanzar ValueError."""
        with pytest.raises(ValueError, match="El tiempo de llegada debe ser un entero no negativo"):
            Proceso("P1", 10, 1, tiempo_llegada=-1)
    
    def test_reiniciar_proceso(self):
        """Test: Reiniciar proceso restaura sus valores iniciales."""
        proceso = Proceso("P1", 10, 1)
        proceso.tiempo_restante = 5
        proceso.tiempo_inicio = 10
        proceso.tiempo_fin = 20
        
        proceso.reiniciar()
        
        assert proceso.tiempo_restante == 10
        assert proceso.tiempo_inicio is None
        assert proceso.tiempo_fin is None
    
    def test_to_dict(self):
        """Test: Conversión a diccionario."""
        proceso = Proceso("P1", 10, 1, tiempo_llegada=5)
        datos = proceso.to_dict()
        
        assert datos['pid'] == "P1"
        assert datos['duracion'] == 10
        assert datos['prioridad'] == 1
        assert datos['tiempo_llegada'] == 5
    
    def test_from_dict(self):
        """Test: Creación desde diccionario."""
        datos = {
            'pid': 'P2',
            'duracion': 15,
            'prioridad': 2,
            'tiempo_llegada': 3
        }
        proceso = Proceso.from_dict(datos)
        
        assert proceso.pid == "P2"
        assert proceso.duracion == 15
        assert proceso.prioridad == 2
        assert proceso.tiempo_llegada == 3
    
    def test_from_dict_sin_tiempo_llegada(self):
        """Test: Creación desde diccionario sin tiempo de llegada usa 0 por defecto."""
        datos = {
            'pid': 'P3',
            'duracion': 8,
            'prioridad': 1
        }
        proceso = Proceso.from_dict(datos)
        
        assert proceso.tiempo_llegada == 0
    
    def test_repr(self):
        """Test: Representación del proceso."""
        proceso = Proceso("P1", 10, 1)
        repr_str = repr(proceso)
        
        assert "P1" in repr_str
        assert "10" in repr_str
        assert "1" in repr_str
    
    def test_str(self):
        """Test: String legible del proceso."""
        proceso = Proceso("P1", 10, 1)
        str_repr = str(proceso)
        
        assert "P1" in str_repr
        assert "10" in str_repr
