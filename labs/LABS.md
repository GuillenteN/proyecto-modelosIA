# Índice de laboratorios ejecutables

> Todos los comandos se ejecutan desde la **carpeta raíz del repositorio**.
> `[Conda]` = requiere `conda activate robots-expertos-mia`
> `[Docker]` = requiere la imagen Docker y ejecutarse dentro del contenedor

---

## Lab 1 — Fundamentos de Robótica y Hardware

| Script | Entorno | Comando |
|---|---|---|
| `lab_1_1_morfologias_dof.py` | \[Conda\] | `python labs/lab_1/lab_1_1_morfologias_dof.py` |
| `lab_1_2a_ik_2d.py` | \[Conda\] | `python labs/lab_1/lab_1_2a_ik_2d.py` |
| `lab_1_2b_jacobiano_numerico.py` | \[Conda\] | `python labs/lab_1/lab_1_2b_jacobiano_numerico.py` |
| `lab_1_3_benchmark_cpu_gpu.py` | \[Conda\] | `python labs/lab_1/lab_1_3_benchmark_cpu_gpu.py` |
| `lab_1_validacion_entorno.py` | \[Docker\] | `./labs/lab_1/shell/04_validate_env.sh` |

### Scripts de automatización Docker (shell/)

| Script | Qué hace |
|---|---|
| `01_install_docker_ubuntu.sh` | Instala Docker en Ubuntu 22.04 |
| `02_enable_docker_without_sudo.sh` | Permite usar Docker sin `sudo` |
| `03_build_image_v1.sh` | Script de compatibilidad; redirige a la construcción de `ros2-curso:v2` |
| `04_validate_env.sh` | Valida el entorno completo dentro del contenedor `ros2-curso:v2` |

---

## Lab 2 — Programación y Simulación con ROS 2

> Todos los scripts Python de este lab se ejecutan **dentro del contenedor**. Flujo recomendado: `docker compose up -d ros2_v1` y después `docker compose exec ros2_v1 bash`.

| Script | Entorno | Comando (dentro del contenedor) |
|---|---|---|
| `lab_2_4_nodo_seguridad.py` | \[Docker v1\] | `python3 /workspace_repo/labs/lab_2/lab_2_4_nodo_seguridad.py` |

### Scripts de automatización Docker (shell/)

| Script | Qué hace |
|---|---|
| `01_ros2_graph_inspection.sh` | Lanza el nodo talker y muestra comandos de inspección del grafo (Lab 2.2) |
| `01_build_image_v2.sh` | **Construye la única imagen final `ros2-curso:v2`** |
| `02_run_turtlebot3_sim.sh` | Abre contenedor v2 con acceso gráfico |
| `03_check_scan_topics.sh` | Comprueba los tópicos del LiDAR |

---

## Lab 3 — Sistemas Expertos y Lógica de Decisión

> Python puro — no requiere Docker. Solo `conda activate robots-expertos-mia`.

| Script | Dependencias | Comando |
|---|---|---|
| `lab_3_1_identificacion_reglas.py` | Ninguna (Python estándar) | `python labs/lab_3/lab_3_1_identificacion_reglas.py` |
| `lab_3_2_motor_inferencia_basico.py` | Ninguna (Python estándar) | `python labs/lab_3/lab_3_2_motor_inferencia_basico.py` |
| `lab_3_3_backward_chaining.py` | Ninguna (Python estándar) | `python labs/lab_3/lab_3_3_backward_chaining.py` |
| `lab_3_4_controlador_difuso.py` | `scikit-fuzzy`, `numpy`, `matplotlib` | `python labs/lab_3/lab_3_4_controlador_difuso.py` |
| `lab_3_5_sistema_experto_salud.py` | Ninguna (Python estándar) | `python labs/lab_3/lab_3_5_sistema_experto_salud.py` |

---

## Lab 4 — Integración: El Robot Autónomo Inteligente

| Script | Dependencias | Comando |
|---|---|---|
| `lab_4_1_deriva_odometria.py` | `numpy`, `matplotlib` | `python labs/lab_4/lab_4_1_deriva_odometria.py` |
| `lab_4_2_interfaz_llm_experto.py` | Solo stdlib (sin API key); `anthropic` u `ollama` opcionales | `python labs/lab_4/lab_4_2_interfaz_llm_experto.py` |

---

## Proyecto Final

> No se proporciona una solucion ejecutable en este repositorio.
> Cada grupo debe desarrollar el proyecto final desde cero usando los Labs 1-4.
> Las 4 propuestas de proyecto estan descritas en `README.md` y en `AIB1_UT0405.pdf`.
