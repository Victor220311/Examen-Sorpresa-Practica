"""
Pruebas unitarias para el repositorio de procesos y persistencia.
"""

import pytest
import sys
import os
import json
import tempfile

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from proceso import Proceso
from repositorio import RepositorioProcesos


class TestRepositorioProcesos:
    """Tests para el repositorio de procesos."""
    
    def test_repositorio_vacio_inicial(self):
        """Test: Repositorio inicia vacío."""
        repo = RepositorioProcesos()
        assert repo.cantidad_procesos() == 0
        assert repo.listar_procesos() == []
    
    def test_agregar_proceso_valido(self):
        """Test: Agregar un proceso válido."""
        repo = RepositorioProcesos()
        proceso = Proceso("P1", 10, 1)
        
        resultado = repo.agregar_proceso(proceso)
        
        assert resultado is True
        assert repo.cantidad_procesos() == 1
    
    def test_agregar_proceso_duplicado(self):
        """Test: No se puede agregar proceso con PID duplicado."""
        repo = RepositorioProcesos()
        proceso1 = Proceso("P1", 10, 1)
        proceso2 = Proceso("P1", 5, 2)
        
        repo.agregar_proceso(proceso1)
        resultado = repo.agregar_proceso(proceso2)
        
        assert resultado is False
        assert repo.cantidad_procesos() == 1
    
    def test_agregar_objeto_invalido(self):
        """Test: Agregar objeto no-Proceso lanza ValueError."""
        repo = RepositorioProcesos()
        
        with pytest.raises(ValueError, match="El objeto debe ser una instancia de Proceso"):
            repo.agregar_proceso("no es un proceso")
    
    def test_obtener_proceso_existente(self):
        """Test: Obtener un proceso por PID."""
        repo = RepositorioProcesos()
        proceso = Proceso("P1", 10, 1)
        repo.agregar_proceso(proceso)
        
        recuperado = repo.obtener_proceso("P1")
        
        assert recuperado is not None
        assert recuperado.pid == "P1"
        assert recuperado.duracion == 10
    
    def test_obtener_proceso_inexistente(self):
        """Test: Obtener proceso inexistente retorna None."""
        repo = RepositorioProcesos()
        
        resultado = repo.obtener_proceso("P999")
        
        assert resultado is None
    
    def test_eliminar_proceso_existente(self):
        """Test: Eliminar un proceso existente."""
        repo = RepositorioProcesos()
        proceso = Proceso("P1", 10, 1)
        repo.agregar_proceso(proceso)
        
        resultado = repo.eliminar_proceso("P1")
        
        assert resultado is True
        assert repo.cantidad_procesos() == 0
    
    def test_eliminar_proceso_inexistente(self):
        """Test: Eliminar proceso inexistente retorna False."""
        repo = RepositorioProcesos()
        
        resultado = repo.eliminar_proceso("P999")
        
        assert resultado is False
    
    def test_listar_procesos(self):
        """Test: Listar todos los procesos."""
        repo = RepositorioProcesos()
        p1 = Proceso("P1", 10, 1)
        p2 = Proceso("P2", 5, 2)
        p3 = Proceso("P3", 8, 1)
        
        repo.agregar_proceso(p1)
        repo.agregar_proceso(p2)
        repo.agregar_proceso(p3)
        
        procesos = repo.listar_procesos()
        
        assert len(procesos) == 3
        pids = [p.pid for p in procesos]
        assert "P1" in pids
        assert "P2" in pids
        assert "P3" in pids
    
    def test_limpiar_repositorio(self):
        """Test: Limpiar elimina todos los procesos."""
        repo = RepositorioProcesos()
        repo.agregar_proceso(Proceso("P1", 10, 1))
        repo.agregar_proceso(Proceso("P2", 5, 2))
        
        repo.limpiar()
        
        assert repo.cantidad_procesos() == 0
    
    def test_guardar_cargar_json(self):
        """Test: Guardar y cargar procesos en formato JSON."""
        repo = RepositorioProcesos()
        repo.agregar_proceso(Proceso("P1", 10, 1, tiempo_llegada=0))
        repo.agregar_proceso(Proceso("P2", 5, 2, tiempo_llegada=2))
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            archivo = f.name
        
        try:
            # Guardar
            repo.guardar_json(archivo)
            
            # Crear nuevo repositorio y cargar
            repo2 = RepositorioProcesos()
            repo2.cargar_json(archivo)
            
            # Verificar
            assert repo2.cantidad_procesos() == 2
            p1 = repo2.obtener_proceso("P1")
            assert p1 is not None
            assert p1.duracion == 10
            assert p1.prioridad == 1
            
            p2 = repo2.obtener_proceso("P2")
            assert p2 is not None
            assert p2.duracion == 5
            assert p2.prioridad == 2
        
        finally:
            # Limpiar archivo temporal
            if os.path.exists(archivo):
                os.remove(archivo)
    
    def test_guardar_cargar_csv(self):
        """Test: Guardar y cargar procesos en formato CSV."""
        repo = RepositorioProcesos()
        repo.agregar_proceso(Proceso("P1", 10, 1))
        repo.agregar_proceso(Proceso("P2", 5, 2))
        repo.agregar_proceso(Proceso("P3", 8, 3))
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            archivo = f.name
        
        try:
            # Guardar
            repo.guardar_csv(archivo)
            
            # Crear nuevo repositorio y cargar
            repo2 = RepositorioProcesos()
            repo2.cargar_csv(archivo)
            
            # Verificar
            assert repo2.cantidad_procesos() == 3
            p1 = repo2.obtener_proceso("P1")
            assert p1 is not None
            assert p1.duracion == 10
            
            p3 = repo2.obtener_proceso("P3")
            assert p3 is not None
            assert p3.prioridad == 3
        
        finally:
            # Limpiar archivo temporal
            if os.path.exists(archivo):
                os.remove(archivo)
    
    def test_cargar_json_reemplaza_existentes(self):
        """Test: Cargar JSON reemplaza procesos existentes."""
        repo = RepositorioProcesos()
        repo.agregar_proceso(Proceso("P_OLD", 100, 99))
        
        # Crear archivo temporal con datos diferentes
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            archivo = f.name
            json.dump([{'pid': 'P_NEW', 'duracion': 5, 'prioridad': 1, 'tiempo_llegada': 0}], f)
        
        try:
            repo.cargar_json(archivo)
            
            assert repo.cantidad_procesos() == 1
            assert repo.obtener_proceso("P_OLD") is None
            assert repo.obtener_proceso("P_NEW") is not None
        
        finally:
            if os.path.exists(archivo):
                os.remove(archivo)
    
    def test_cargar_json_archivo_inexistente(self):
        """Test: Cargar JSON inexistente lanza IOError."""
        repo = RepositorioProcesos()
        
        with pytest.raises(IOError, match="Archivo no encontrado"):
            repo.cargar_json("archivo_que_no_existe.json")
    
    def test_cargar_csv_archivo_inexistente(self):
        """Test: Cargar CSV inexistente lanza IOError."""
        repo = RepositorioProcesos()
        
        with pytest.raises(IOError, match="Archivo no encontrado"):
            repo.cargar_csv("archivo_que_no_existe.csv")
    
    def test_len_repositorio(self):
        """Test: Operador len() funciona con el repositorio."""
        repo = RepositorioProcesos()
        repo.agregar_proceso(Proceso("P1", 10, 1))
        repo.agregar_proceso(Proceso("P2", 5, 2))
        
        assert len(repo) == 2
