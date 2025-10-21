# Sistema de Planificación de Procesos - Práctica de Ingeniería Informática

## Descripción General

En este ejercicio aplicaremos conceptos clave de Ingeniería Informática mediante Python y programación orientada a objetos, sin interfaz gráfica, con persistencia de datos y pruebas unitarias. Modelaremos un entorno simplificado de un sistema operativo donde se crean y gestionan procesos (o "trabajos") y se programa su ejecución mediante un planificador de CPU (scheduler). 

El alumno deberá diseñar clases que representen procesos, un scheduler que implemente distintos algoritmos (por ejemplo, FCFS, Round-Robin) y un repositorio que mantenga el conjunto de procesos, además de serializar la información en disco.

---

## 🎯 Objetivos de Evaluación

Este ejercicio evalúa:

- ✅ Diseño de clases claras y cohesivas
- ✅ Implementación de algoritmos de planificación de procesos
- ✅ Persistencia de datos en CSV o JSON
- ✅ Organización profesional del proyecto (estructura, entornos, documentación)
- ✅ Cobertura con pruebas unitarias

Este ejercicio evaluará la capacidad del alumno para:

1. Diseñar clases claras, cohesionadas y orientadas a objetos
2. Implementar algoritmos de planificación de procesos
3. Utilizar mecanismos de persistencia (archivos CSV o JSON)
4. Organizar adecuadamente el código fuente y las pruebas
5. Aplicar pruebas unitarias para verificar el correcto funcionamiento
6. Documentar y preparar el proyecto para ejecución profesional

---

## 📋 Requisitos Funcionales

### 1. Registro de Procesos
- Cada proceso tiene un **PID** (identificador único), **duración de CPU** (tiempo de ejecución requerido), y **prioridad** (entero; menor = más urgente)
- No puede haber dos procesos con el mismo PID

### 2. Listado de Procesos
- Mostrar todos los procesos registrados con sus atributos

### 3. Planificación y Simulación
Implementar al menos dos algoritmos de planificación de CPU:
- **FCFS** (First-Come, First-Served)
- **Round-Robin** con quantum configurable

El scheduler debe recibir la cola de procesos y simular su ejecución, produciendo:
- Un **diagrama de Gantt** (lista de tuplas de `(PID, tiempo_inicio, tiempo_fin)`)
- **Métricas**:
  - Tiempo de respuesta medio
  - Tiempo de espera medio
  - Tiempo de retorno medio

### 4. Persistencia
- Guardar y cargar la lista de procesos desde un archivo **CSV** o **JSON**

### 5. Pruebas Unitarias
- Carpeta `tests/` con pruebas para creación, manipulación, planificación y persistencia

### 6. Estructura Profesional
- Separar el código en `src/` y pruebas en `tests/`
- Incluir `README.md` y `requirements.txt`
- Uso de entorno virtual

---

## 📦 Entrega Esperada

- Proyecto comprimido (`.zip`) con toda la estructura descrita
- Código funcional, comentado y limpio
- Pruebas unitarias completas y ejecutables
- Persistencia verificada mediante archivos de prueba
- Informe o README que explique cómo ejecutar el proyecto y las pruebas

---

## 🔧 Desarrollo del Proyecto

### Parte 1: Modelado de Procesos

Implementa una clase **`Proceso`** que represente un proceso del sistema.

**Atributos obligatorios:**
- `pid`: identificador único del proceso (string, no vacío)
- `duracion`: cantidad total de tiempo de CPU requerida (entero positivo)
- `prioridad`: valor entero que indique la urgencia del proceso (a menor valor, mayor prioridad)

**Validación:**
- Se debe validar que `pid` no esté duplicado al crear un nuevo proceso

**Atributos adicionales sugeridos:**
- `tiempo_restante`: para uso interno del scheduler
- `tiempo_llegada`: asumido como 0 para simplificación
- `tiempo_inicio` y `tiempo_fin`: para cálculo de métricas

---

### Parte 2: Planificadores de CPU

#### 2.1 Interfaz General
Diseña una clase abstracta **`Scheduler`** que defina la interfaz del planificador.

Debe incluir el método abstracto:
```python
def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]
```
donde `GanttEntry` es una tupla `(pid, tiempo_inicio, tiempo_fin)`.

#### 2.2 Algoritmo FCFS
Implementa una clase **`FCFSScheduler`** que planifique los procesos según el orden de llegada (First-Come, First-Served).

#### 2.3 Algoritmo Round-Robin
Implementa una clase **`RoundRobinScheduler`** que use planificación con quantum fijo, configurable por parámetro.

El algoritmo debe recorrer los procesos en ciclos, restando el tiempo ejecutado a cada proceso hasta que todos hayan finalizado.

---

### Parte 3: Repositorio de Procesos y Persistencia

#### 3.1 Repositorio de Procesos
Implementa una clase **`RepositorioProcesos`** que gestione el conjunto de procesos activos.

**Funciones mínimas requeridas:**
- Agregar proceso (verificando unicidad de pid)
- Listar todos los procesos registrados
- Eliminar un proceso por su pid
- Obtener un proceso dado su pid

#### 3.2 Persistencia
Implementa métodos para guardar y cargar el conjunto de procesos usando:
- Archivos en formato **JSON**
- Archivos en formato **CSV** (separador: `;`)

Al cargar un archivo, los procesos existentes deben ser reemplazados.

---

### Parte 4: Simulación y Métricas

#### 4.1 Ejecución Simulada
El scheduler debe producir una lista de ejecuciones (diagrama de Gantt) que muestre:
- El orden de ejecución
- El tiempo de inicio y fin de cada tramo de proceso

#### 4.2 Cálculo de Métricas
Calcula, para cada proceso y de forma agregada:
- **Tiempo de respuesta** = `tiempo_inicio − tiempo_llegada`
- **Tiempo de retorno** = `tiempo_fin − tiempo_llegada`
- **Tiempo de espera** = `tiempo_retorno − duración`

Presenta los valores promedio para el conjunto de procesos planificados.

---

### Parte 5: Pruebas Unitarias

Crea una carpeta `tests/` que contenga pruebas automáticas usando **pytest**.

Las pruebas deben incluir casos para:
- Creación y validación de procesos
- Comportamiento de los algoritmos de planificación
- Persistencia de procesos en archivos JSON y CSV
- Cálculo correcto de métricas a partir de Gantt conocido

---

### Parte 6: Organización del Proyecto

El proyecto debe tener la siguiente estructura mínima:

```
proyecto-scheduler/
├─ src/
│  ├─ proceso.py
│  ├─ scheduler.py
│  ├─ repositorio.py
│  ├─ metrics.py
│  └─ main.py       # Opcional: CLI
├─ tests/
│  ├─ test_proceso.py
│  ├─ test_scheduler.py
│  ├─ test_repositorio.py
│  └─ test_metrics.py
├─ requirements.txt
└─ README.md
```

**Instrucciones:**
- Instrucciones de uso y pruebas deben estar en `README.md`
- Usa un entorno virtual (`venv`) y lista las dependencias necesarias en `requirements.txt`

---

### Parte 7: Interfaz Opcional (main.py)

Puedes agregar una interfaz en línea de comandos (`main.py`) que permita:
- Agregar y listar procesos
- Seleccionar algoritmo de planificación
- Ejecutar simulaciones y mostrar resultados
- Guardar y cargar procesos
- Salir del programa

---

## 📊 Criterios de Evaluación

| Criterio | Ponderación |
|----------|-------------|
| Correcto modelado de clases orientadas a objetos | 20% |
| Implementación de algoritmos FCFS y Round-Robin | 20% |
| Persistencia en archivos JSON/CSV | 15% |
| Cálculo y precisión de métricas | 15% |
| Pruebas unitarias automatizadas | 15% |
| Organización del proyecto y documentación | 15% |

**Total: 100%**

---

## 🚀 Instrucciones de Ejecución

### Preparación del entorno
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar el programa principal
```bash
python src/main.py
```

### Ejecutar pruebas unitarias
```bash
pytest tests/ -v
```

---

## 📚 Recursos y Conceptos Clave

- **Planificación de CPU**: Algoritmos que determinan qué proceso ejecutar en cada momento
- **FCFS**: El primer proceso en llegar es el primero en ejecutarse
- **Round-Robin**: Cada proceso recibe un quantum de tiempo de forma cíclica
- **Diagrama de Gantt**: Representación visual de la secuencia de ejecución de procesos
- **Persistencia**: Almacenamiento permanente de datos en archivos

---

## 📝 Notas Adicionales

- El proyecto debe ser entregado como archivo `.zip` con toda la estructura descrita
- El código debe estar comentado y seguir buenas prácticas de programación
- Las pruebas deben cubrir los casos principales y edge cases
- La documentación debe ser clara y completa

---

**Fecha de Entrega:** [Especificar fecha]  
**Modalidad:** Individual  
**Formato:** Proyecto comprimido (.zip)