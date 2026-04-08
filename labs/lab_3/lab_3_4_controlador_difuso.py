#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


distancia = ctrl.Antecedent(np.arange(0, 3.1, 0.01), "distancia")
velocidad = ctrl.Consequent(np.arange(0, 0.51, 0.01), "velocidad")

distancia["muy_cerca"] = fuzz.trimf(distancia.universe, [0.0, 0.0, 0.5])
distancia["cerca"] = fuzz.trimf(distancia.universe, [0.2, 0.6, 1.0])
distancia["media"] = fuzz.trimf(distancia.universe, [0.7, 1.2, 1.7])
distancia["lejos"] = fuzz.trimf(distancia.universe, [1.4, 2.0, 2.6])
distancia["muy_lejos"] = fuzz.trimf(distancia.universe, [2.3, 3.0, 3.0])

velocidad["parado"] = fuzz.trimf(velocidad.universe, [0.00, 0.00, 0.05])
velocidad["lento"] = fuzz.trimf(velocidad.universe, [0.03, 0.10, 0.20])
velocidad["medio"] = fuzz.trimf(velocidad.universe, [0.15, 0.25, 0.35])
velocidad["rapido"] = fuzz.trimf(velocidad.universe, [0.30, 0.40, 0.50])
velocidad["max"] = fuzz.trimf(velocidad.universe, [0.45, 0.50, 0.50])

regla1 = ctrl.Rule(distancia["muy_cerca"], velocidad["parado"])
regla2 = ctrl.Rule(distancia["cerca"], velocidad["lento"])
regla3 = ctrl.Rule(distancia["media"], velocidad["medio"])
regla4 = ctrl.Rule(distancia["lejos"], velocidad["rapido"])
regla5 = ctrl.Rule(distancia["muy_lejos"], velocidad["max"])

sistema_control = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5])
simulacion = ctrl.ControlSystemSimulation(sistema_control)


def main():
    distancias_prueba = [0.1, 0.4, 0.8, 1.5, 2.5]
    print("=== Respuesta del Controlador Difuso ===")
    print(f"{'Distancia (m)':<18} {'Velocidad (m/s)':<18} {'Interpretacion'}")
    print("-" * 55)

    for d in distancias_prueba:
        simulacion.input["distancia"] = d
        simulacion.compute()
        v = simulacion.output["velocidad"]
        if v < 0.05:
            interp = "PARADO"
        elif v < 0.20:
            interp = "movimiento lento"
        elif v < 0.35:
            interp = "velocidad media"
        else:
            interp = "velocidad alta"
        print(f"{d:<18.1f} {v:<18.3f} {interp}")

    rango_distancias = np.arange(0.05, 3.0, 0.05)
    velocidades_salida = []

    for d in rango_distancias:
        simulacion.input["distancia"] = d
        simulacion.compute()
        velocidades_salida.append(simulacion.output["velocidad"])

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(rango_distancias, velocidades_salida, "b-", linewidth=2)
    ax.fill_between(rango_distancias, 0, velocidades_salida, alpha=0.15)
    ax.set_xlabel("Distancia al obstaculo (m)")
    ax.set_ylabel("Velocidad lineal (m/s)")
    ax.set_title("Curva de respuesta del controlador difuso de velocidad")
    ax.grid(True, alpha=0.4)
    ax.axvline(x=0.5, color="r", linestyle="--", alpha=0.6, label="Umbral critico (0.5m)")
    ax.legend()
    plt.tight_layout()
    plt.show()

    print("\nNota: La transicion suave de la curva evita cambios bruscos.")


if __name__ == "__main__":
    main()
