#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np


np.random.seed(42)
N_PASOS = 100
RUIDO_SIGMA = 0.05


def main():
    angulos = np.linspace(0, 2 * np.pi, N_PASOS)
    real_x = np.cos(angulos) * 5
    real_y = np.sin(angulos) * 5

    est_x, est_y = [real_x[0]], [real_y[0]]
    for i in range(1, N_PASOS):
        dx = (real_x[i] - real_x[i - 1]) + np.random.normal(0, RUIDO_SIGMA)
        dy = (real_y[i] - real_y[i - 1]) + np.random.normal(0, RUIDO_SIGMA)
        est_x.append(est_x[-1] + dx)
        est_y.append(est_y[-1] + dy)

    error_final = np.sqrt((real_x[-1] - est_x[-1]) ** 2 + (real_y[-1] - est_y[-1]) ** 2)
    print(f"Error acumulado tras {N_PASOS} pasos: {error_final:.4f} metros")
    print(f"El robot cree estar en ({est_x[-1]:.2f}, {est_y[-1]:.2f})")
    print(f"pero esta realmente en  ({real_x[-1]:.2f}, {real_y[-1]:.2f})")

    umbral_deriva = 0.3
    if error_final > umbral_deriva:
        print(f"\n[REGLA SE] Error ({error_final:.2f}m) > umbral ({umbral_deriva}m)")
        print("           -> Accion: solicitar_relocalizacion_lidar()")

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(real_x, real_y, "b-", linewidth=2, label="Trayectoria real")
    ax.plot(est_x, est_y, "r--", linewidth=1.5, label="Odometria estimada")
    ax.plot(est_x[-1], est_y[-1], "rx", markersize=12, label="Posicion estimada final")
    ax.plot(real_x[-1], real_y[-1], "b*", markersize=12, label="Posicion real final")
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title(f"Deriva de Odometria tras {N_PASOS} pasos | Error: {error_final:.4f} m")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
