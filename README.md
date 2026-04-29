# Proyecto Final: Robot Autónomo Inteligente con Sistema Experto

> **Curso:** Robots Expertos e Inteligencia Artificial  
> **Objetivo:** Integración completa de percepción sensorial, lógica experta y control difuso en un robot autónomo funcional con ROS 2.

## 📋 Índice

- [Descripción General](#descripción-general)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Requisitos del Entorno](#requisitos-del-entorno)
- [Instalación](#instalación)
- [Uso y Ejecución](#uso-y-ejecución)
- [Componentes Principales](#componentes-principales)
- [Flujo de Datos](#flujo-de-datos)
- [Ejemplos de Funcionamiento](#ejemplos-de-funcionamiento)
- [Resolución de Problemas](#resolución-de-problemas)

---

## 📖 Descripción General

Este proyecto integra cuatro laboratorios progresivos (Lab 1-4) en una solución completa de robótica autónoma:

1. **Fundamentos de Robótica** (Lab 1): Cinemática, control de hardware, benchmarking
2. **ROS 2 y Programación** (Lab 2): Nodos, tópicos, servicios, simulación con Gazebo
3. **Sistemas Expertos** (Lab 3): Reglas de decisión, motores de inferencia, lógica difusa
4. **Integración** (Lab 4): Composición completa del robot autónomo

**El resultado:** Un robot TurtleBot3 simulado que:
- ✅ Navega autónomamente detectando obstáculos
- ✅ Toma decisiones basadas en reglas y contexto (Sistema Experto)
- ✅ Controla su velocidad con lógica difusa según distancias
- ✅ Monitorea batería y temperatura con acciones preventivas
- ✅ Mantiene trazabilidad de todas sus decisiones

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                      ROBOT TurtleBot3                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           NODO PERCEPCIÓN (nodo_percepcion.py)          │  │
│  │  • Suscribe: /scan (LiDAR)                              │  │
│  │  • Publica: /estado_entorno (LIBRE/OBSTACULO)           │  │
│  │  • Lógica: Detecta obstáculos en rango frontal         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │       NODO TELEMETRÍA (nodo_telemetria.py)             │  │
│  │  • Simula: Batería, Temperatura                         │  │
│  │  • Publica: /telemetria (JSON)                          │  │
│  │  • Consumo: 0.5% batería por segundo                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │    NODO CEREBRO SE (nodo_cerebro_se.py)               │  │
│  │  • Motor de Reglas (Sistema Experto)                   │  │
│  │  • Entradas: Telemetría + Percepción                  │  │
│  │  • Decisiones:                                          │  │
│  │    - R1: T > 85°C → PARADA_TERMICA                    │  │
│  │    - R2: Batería < 15% → RECARGA                      │  │
│  │    - R3: Obstáculo + Moviendo → EVASION               │  │
│  │  • Publica: /modo_operacion                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │    NODO ACTUACIÓN (nodo_actuacion.py)                 │  │
│  │  • Controlador Difuso (Lab 3.4)                        │  │
│  │  • Entradas: Modo operación + Distancia (LiDAR)       │  │
│  │  • Lógica de Patrulla: A → B → Rotar → Repetir        │  │
│  │  • Publica: /cmd_vel (Twist)                           │  │
│  │  • Ejecución: 20Hz (Muy Reactivo)                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Simulador Gazebo / Robot Real                   │  │
│  │  • Recibe comandos: /cmd_vel                            │  │
│  │  • Genera sensores: /scan, /odom, etc.                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Requisitos del Entorno

### Hardware (Recomendado)
- CPU: Mínimo 4 núcleos
- RAM: 8 GB mínimo (16 GB ideal para simulación)
- GPU: NVIDIA CUDA compatible (opcional, para PyTorch)

### Software
- **Sistema Operativo:** Ubuntu 22.04 LTS (recomendado)
- **Docker:** Versión 20.10+ (para ejecución en contenedor)
- **Docker Compose:** Versión 1.29+
- **Anaconda/Miniconda:** Para gestión de entornos Python

### Dependencias Python

```yaml
# Core
numpy>=1.24
scipy>=1.11
matplotlib>=3.7

# Robótica
torch>=2.1                    # PyTorch para cálculos complejos
pybullet>=3.2                 # Simulación física

# Lógica Difusa
scikit-fuzzy>=0.4.2          # Fuzzy Logic

# IA/LLM (Opcional)
anthropic>=0.39.0            # Claude API
ollama>=0.4.0                # Ollama local LLM

# ROS 2 (dentro del contenedor Docker)
# - rclpy
# - sensor_msgs, geometry_msgs, std_msgs
# - rclcpp (C++)
```

---

## 📦 Instalación

### Opción 1: Ejecución Local (Conda)

```bash
# 1. Clonar/Descargar el repositorio
cd proyecto-modelosIA

# 2. Crear entorno Conda
conda env create -f environment.yml
conda activate robots-expertos-mia

# 3. Instalar dependencias adicionales
pip install -r requirements.txt

# 4. Verificar instalación
python -c "import rclpy; print('✅ ROS 2 listo')"
```

### Opción 2: Ejecución en Docker (Recomendado para ROS 2)

```bash
# 1. Construir la imagen
cd labs/lab_2/shell
bash 01_build_image_v2.sh

# 2. Iniciar contenedor
docker compose up -d ros2_v1

# 3. Acceder al contenedor
docker compose exec ros2_v1 bash

# 4. Dentro del contenedor: lanzar nodos
cd /workspace_repo
python3 labs/proyecto_final/orquestador_final.py
```

### Opción 3: Instalación Manual de ROS 2

```bash
# En Ubuntu 22.04
sudo apt update
sudo apt install -y ros-humble-desktop
source /opt/ros/humble/setup.bash

# Crear workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
source install/setup.bash
```

---

## 🚀 Uso y Ejecución

### Lanzar el Sistema Completo

**Dentro de Docker (Recomendado):**

```bash
# Terminal 1: Iniciar contenedor + Gazebo
docker compose up -d ros2_v2
docker compose exec ros2_v2 bash

# Dentro del contenedor:
source /opt/ros/humble/setup.bash
cd /workspace_repo

# Lanzar simulación Gazebo
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# Terminal 2: En el mismo contenedor
docker compose exec ros2_v2 bash
source /opt/ros/humble/setup.bash
cd /workspace_repo

# Lanzar nodos del proyecto
python3 labs/proyecto_final/nodo_telemetria.py --forzar-bateria-baja  # (Opcional: test de recarga)
```

**Secuencia de Lanzamiento Recomendada:**

```bash
# Terminal 1: Telemetría
python3 labs/proyecto_final/nodo_telemetria.py

# Terminal 2: Percepción
python3 labs/proyecto_final/nodo_percepcion.py

# Terminal 3: Cerebro (Sistema Experto)
python3 labs/proyecto_final/nodo_cerebro_se.py

# Terminal 4: Actuación (Control)
python3 labs/proyecto_final/nodo_actuacion.py
```

### Monitoreo en Tiempo Real

```bash
# Ver todos los tópicos publicados
ros2 topic list

# Escuchar un tópico específico
ros2 topic echo /modo_operacion
ros2 topic echo /estado_entorno
ros2 topic echo /telemetria

# Inspeccionar grafo de nodos
ros2 graph

# Ver velocidades de publicación
ros2 topic hz /cmd_vel
```

---

## 🔧 Componentes Principales

### 1️⃣ **Nodo Percepción** (`nodo_percepcion.py`)

**Responsabilidad:** Convertir datos brutos de sensores en información útil

| Aspecto | Detalle |
|--------|---------|
| **Entrada** | `/scan` (LaserScan) - LiDAR frontal |
| **Salida** | `/estado_entorno` (String: "LIBRE" o "OBSTACULO") |
| **Lógica** | Detecta mínima distancia en rango ±20° del frente |
| **Umbral** | 0.5 metros (configurable) |
| **QoS** | BEST_EFFORT (crítico para Gazebo) |

**Ecuación de Decisión:**
```
IF distancia_minima < 0.5m THEN "OBSTACULO"
ELSE "LIBRE"
```

---

### 2️⃣ **Nodo Telemetría** (`nodo_telemetria.py`)

**Responsabilidad:** Simular estado físico del robot

| Métrica | Simulación |
|---------|-----------|
| **Batería** | -0.5% por segundo; comienza 100% |
| **Temperatura** | Gaussiana: μ=70°C, σ=8°C |
| **Frecuencia** | 1 Hz |
| **Formato** | JSON: `{bateria, temperatura, status}` |

**Opciones Especiales:**
```bash
# Forzar batería baja para testing
python3 nodo_telemetria.py --forzar-bateria-baja  # Batería inicia en 10%
```

---

### 3️⃣ **Nodo Cerebro - Sistema Experto** (`nodo_cerebro_se.py`)

**Responsabilidad:** Tomar decisiones basadas en lógica experta

**Reglas (Motor de Inferencia):**

| Prioridad | Regla | Condición | Acción |
|-----------|-------|-----------|--------|
| 1 (↑ Alta) | **Térmica** | `T > 85°C` | `PARADA_TERMICA` |
| 2 | **Supervivencia** | `Batería < 15%` | `RECARGA` |
| 3 | **Navegación** | `Obstáculo = OBSTACULO` | `EVASION` |
| 4 (↓ Default) | — | — | `TRANSPORTE` |

**Flujo de Decisión:**
```python
IF temperatura > 85°C:
    modo = PARADA_TERMICA  # ¡Parar inmediatamente!
ELIF bateria < 15:
    modo = RECARGA         # Buscar base de recarga
ELIF estado_percepcion == OBSTACULO AND modo == TRANSPORTE:
    modo = EVASION         # Esquivar obstáculo
ELSE:
    modo = TRANSPORTE      # Continuar misión
```

---

### 4️⃣ **Nodo Actuación** (`nodo_actuacion.py`)

**Responsabilidad:** Ejecutar acciones de movimiento

**Componentes:**

| Componente | Función |
|-----------|---------|
| **Controlador Difuso** | Mapea distancia → velocidad lineal |
| **Lógica de Patrulla** | Robot va A → B → Rota → Repite |
| **Gestor de Modos** | Ejecuta acciones según `/modo_operacion` |
| **Frecuencia** | 20 Hz (muy reactivo) |

**Controlador Difuso (Fuzzy Logic):**

```
Entrada: Distancia (metros)
┌─────────────────────────────────────────┐
│ muy_cerca  → parado       (dist < 0.5)  │
│ cerca      → lento        (dist 0.2-1.0)│
│ media      → medio        (dist 0.7-1.7)│
│ lejos      → rápido       (dist 1.4-2.6)│
│ muy_lejos  → máximo       (dist > 2.3)  │
└─────────────────────────────────────────┘
        ↓
Salida: Velocidad lineal (0-1.0 m/s)
```

**Estados de Actuación:**

```
TRANSPORTE:        linear.x = fuzzy_output, angular.z = 0
EVASION:           Gira ±30° mientras retrocede
RECARGA:           Se detiene (espera en base)
PARADA_TERMICA:    Se detiene inmediatamente (emergencia)
```

---

## 📊 Flujo de Datos

```
┌─────────────────┐
│   Simulador     │
│   Gazebo        │
│   (LiDAR + IMU) │
└────────┬────────┘
         │
         ↓ /scan
    ┌─────────────────────┐
    │ Nodo Percepción     │
    │ Detecta Obstáculos  │
    └────────┬────────────┘
             │
             ↓ /estado_entorno (LIBRE/OBSTACULO)
             │
    ┌────────▼────────────┬──────────────────┐
    │                     │                  │
    │ /telemetria         │ /estado_entorno  │
    │ (Nodo Telemetría)   │ (Nodo Percepción)│
    │                     │                  │
    └────────┬────────────┴────────┬─────────┘
             │                     │
             └─────────┬───────────┘
                       ↓
        ┌──────────────────────────────┐
        │ Nodo Cerebro SE              │
        │ Motor de Inferencia (Reglas) │
        └──────────┬───────────────────┘
                   │
                   ↓ /modo_operacion
    ┌──────────────────────────────────┐
    │ Nodo Actuación                   │
    │ Controlador Difuso + Movimiento  │
    └──────────┬───────────────────────┘
               │
               ↓ /cmd_vel (Twist)
    ┌──────────────────────────────────┐
    │ Simulador / Robot Real           │
    │ TurtleBot3 - Motor Control       │
    └──────────────────────────────────┘
```

---

## 💡 Ejemplos de Funcionamiento

### Escenario 1: Navegación Normal

```
[NodoTelemetria]  Pub: {"bateria": 95.5, "temperatura": 71.2, "status": "OK"}
[NodoPercepcion]  [LIBRE] Min: 2.15m | Lecturas válidas: 41
[NodoCerebroSE]   Estado: T:71.2 B:95.5 Obs:LIBRE → MODO: TRANSPORTE
[NodoActuacion]   TRANSPORTE: Avanzando (v=0.8 m/s)
```

**Comportamiento esperado:** Robot avanza hacia adelante a velocidad media

---

### Escenario 2: Detección de Obstáculo

```
[NodoPercepcion]  [OBSTACULO] Min: 0.35m | Lecturas válidas: 41
[NodoCerebroSE]   Estado: T:70.1 B:92.3 Obs:OBSTACULO → MODO: EVASION
[NodoActuacion]   EVASION: Girando 30° CCW + Retrocediendo
```

**Comportamiento esperado:** Robot esquiva el obstáculo

---

### Escenario 3: Batería Baja (Test)

```bash
# Lanzar con batería forzada a 10%
python3 nodo_telemetria.py --forzar-bateria-baja
```

```
[NodoTelemetria]  Pub: {"bateria": 9.8, "temperatura": 68.5, "status": "CRITICAL"}
[NodoCerebroSE]   Estado: T:68.5 B:9.8 Obs:LIBRE → MODO: RECARGA
[NodoActuacion]   RECARGA: Robot detenido esperando en base
```

**Comportamiento esperado:** Robot se detiene completamente

---

### Escenario 4: Pico de Temperatura (Emergencia)

```
[NodoTelemetria]  Pub: {"bateria": 60.0, "temperatura": 87.3, "status": "CRITICAL"}
[NodoCerebroSE]   Estado: T:87.3 B:60.0 Obs:LIBRE → MODO: PARADA_TERMICA
[NodoActuacion]   !!! EXCESO TEMPERATURA !!! Robot completamente detenido
```

**Comportamiento esperado:** Parada inmediata de emergencia

---

## 🐛 Resolución de Problemas

### Problema 1: `ModuleNotFoundError: No module named 'rclpy'`

**Causa:** ROS 2 no instalado o entorno Python incorrecto

**Solución:**
```bash
# En Docker
docker compose exec ros2_v1 bash
source /opt/ros/humble/setup.bash

# Local (Ubuntu)
source /opt/ros/humble/setup.bash
```

---

### Problema 2: `QoS mismatch` en LiDAR

**Causa:** Incompatibilidad de Quality of Service entre Gazebo y nodos

**Solución:** Ya implementada en `nodo_percepcion.py`:
```python
qos_perfil = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=10
)
```

---

### Problema 3: El robot no se mueve en Gazebo

**Causa:** Nodos no conectados correctamente o `/cmd_vel` no subscrito

**Verificar:**
```bash
ros2 topic list                    # ¿Existe /cmd_vel?
ros2 topic hz /cmd_vel             # ¿Se publica?
ros2 node list                     # ¿Están todos los nodos?
ros2 graph                         # ¿Grafo conectado?
```

---

### Problema 4: LiDAR sin datos (`/scan` vacío)

**Causa:** Gazebo no lanzado o modelo TurtleBot3 no cargado

**Solución:**
```bash
# Dentro del contenedor
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

---

## 📚 Referencias a Labs

Este proyecto integra:

- **Lab 1:** Fundamentos de robótica en `nodo_actuacion.py` (cinemática)
- **Lab 2:** ROS 2 en todos los nodos (pub/sub, servicios)
- **Lab 3:** Sistema Experto en `nodo_cerebro_se.py` + Fuzzy en `nodo_actuacion.py`
- **Lab 4:** Integración completa en arquitectura de 4 nodos

Para detalles específicos, ver [labs/LABS.md](labs/LABS.md)

---

## 📝 Licencia

Proyecto académico del Curso de Robots Expertos e Inteligencia Artificial.
