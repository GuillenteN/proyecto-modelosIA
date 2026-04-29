# 🤖 Proyecto Final: Arquitectura Híbrida de Navegación Autónoma en ROS 2

Este repositorio contiene la implementación integral del proyecto final para la asignatura de **Modelos de IA**. El sistema permite a un robot móvil realizar patrullas cíclicas entre dos puntos de interés (A <-> B) integrando un **Sistema Experto (SBR)** para la toma de decisiones y un **Controlador Difuso** para el movimiento.

---

## 1. Introducción y Objetivos
El objetivo principal es desarrollar un sistema de navegación robusto bajo el middleware **ROS 2 Humble**. A diferencia de los sistemas de navegación convencionales, esta solución utiliza un enfoque híbrido:
1.  **Capa de Seguridad (Sistema Experto):** Supervisa el hardware y el entorno para decidir *qué* debe hacer el robot en cada momento.
2.  **Capa de Ejecución (Lógica Difusa):** Gestiona *cómo* se mueve el robot basándose en la proximidad de obstáculos, evitando frenazos bruscos.

---

## 2. Arquitectura del Sistema (Grafo de Nodos)
El sistema está desacoplado en cuatro unidades lógicas funcionales que se comunican de forma asíncrona mediante tópicos:

* **`nodo_percepcion`**: Suscribe al tópico `/scan` (LiDAR). Procesa los rangos frontales para detectar colisiones inminentes y publica en `/estado_entorno`.
* **`nodo_telemetria`**: Simula el consumo de batería (descarga de 0.5% por tick) y la temperatura (distribución gaussiana $\mu=70, \sigma=8$). Publica en formato JSON en `/telemetria`.
* **`nodo_cerebro_se`**: Motor de inferencia que procesa los datos de los sensores y determina el modo de operación (`TRANSPORTE`, `EVASION`, `RECARGA`, `PARADA_TERMICA`).
* **`nodo_actuacion`**: Implementa la máquina de estados de la ruta A-B y utiliza el controlador borroso para publicar en `/cmd_vel`.

---

## 3. Motor de Decisiones: Sistema Experto (SE)
El cerebro del robot utiliza un razonamiento de encadenamiento hacia adelante (Forward Chaining) basado en la siguiente tabla de prioridades:

| Prioridad | Condición (Antecedente) | Modo Resultante | Acción Mecánica |
| :--- | :--- | :--- | :--- |
| **1 (Crítica)** | `Temperatura > 85°C` | `PARADA_TERMICA` | Bloqueo inmediato de motores. |
| **2 (Alta)** | `Batería < 15%` | `RECARGA` | Parada total para mantenimiento. |
| **3 (Media)** | `Obstáculo == TRUE` | `EVASION` | Giro sobre eje propio (evitar colisión). |
| **4 (Baja)** | `Estado Nominal` | `TRANSPORTE` | Ejecución de ruta A <-> B. |

---

## 4. Control de Movimiento: Lógica Difusa
Para el desplazamiento en el modo `TRANSPORTE`, se emplea un sistema de control borroso de tipo Mamdani (basado en el Lab 3.4) para que el robot vaya "to follado" pero seguro.

### 4.1. Variables Lingüísticas
* **Entrada (Distancia):** *Muy Cerca, Cerca, Media, Lejos, Muy Lejos*.
* **Salida (Velocidad):** *Parado, Lento, Medio, Rápido, Max*.

El sistema realiza la defuzzificación por el método del centroide, garantizando que el robot ajuste su velocidad lineal de forma fluida según la distancia al obstáculo más cercano detectado por el LiDAR.

---

## 5. Validación Experimental
Se han documentado los resultados de las pruebas de estrés realizadas en el entorno Docker:

### 5.1. Prueba de Validación Forzada (Batería)
Utilizando el parámetro `--forzar-bateria-baja`, el nodo de telemetría inicia directamente en el 10%. 
* **Resultado:** El sistema experto transicionó a modo `RECARGA` en menos de 0.5s, deteniendo el robot exitosamente antes de iniciar la misión.

### 5.2. Prueba de Seguridad Térmica
Forzado de temperatura a 90°C durante la navegación activa.
* **Resultado:** El robot clava frenos y publica una advertencia de estado crítico, ignorando cualquier otra entrada sensorial o comando de ruta.

### 5.3. Prueba de Ruta A-B y Velocidad
Configuración del controlador con $V_{max} = 1.0 \text{ m/s}$.
* **Resultado:** El robot completa la ruta de ida y vuelta de forma fluida. Se observa que la velocidad se reduce suavemente al acercarse a los límites del tramo o si se interpone un objeto.

---

## 6. Limitaciones y Reflexión
1.  **Deriva Temporal:** Al no utilizar un sistema de odometría real o SLAM, la ruta basada en tiempos (`time.time()`) puede presentar deriva tras varios ciclos de funcionamiento.
2.  **Dependencias de Entorno:** El sistema requiere la instalación manual de `scikit-fuzzy` y `networkx` dentro del contenedor ROS 2 para su correcto funcionamiento.
3.  **Modularidad:** La arquitectura es altamente modular; se podrían añadir reglas de misión adicionales (ej. detección de incendios o personas) sin modificar el nodo de actuación física.

---

## 🛠️ Instalación y Uso

### Prerrequisitos
Dentro del contenedor de ROS 2, instalar las dependencias de Python:
```bash
pip install scikit-fuzzy networkx
