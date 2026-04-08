#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


def resolver_ik_simple(target_x, target_y, l1, l2):
    d_sq = target_x**2 + target_y**2
    d = np.sqrt(d_sq)

    if d > (l1 + l2):
        return None, f"Objetivo ({target_x}, {target_y}) fuera de alcance (max: {l1 + l2})"
    if d < abs(l1 - l2):
        return None, f"Objetivo ({target_x}, {target_y}) demasiado cercano (min: {abs(l1 - l2)})"

    cos_theta2 = (d_sq - l1**2 - l2**2) / (2 * l1 * l2)
    theta2 = np.arccos(np.clip(cos_theta2, -1, 1))

    alpha = np.arctan2(target_y, target_x)
    beta = np.arctan2(l2 * np.sin(theta2), l1 + l2 * np.cos(theta2))
    theta1 = alpha - beta

    return np.degrees([theta1, theta2]), "Exito"


def visualizar_brazo(target_x, target_y, l1, l2, angulos):
    theta1_rad = np.radians(angulos[0])
    theta2_rad = np.radians(angulos[1])

    p0 = np.array([0, 0])
    p1 = p0 + l1 * np.array([np.cos(theta1_rad), np.sin(theta1_rad)])
    p2 = p1 + l2 * np.array([
        np.cos(theta1_rad + theta2_rad),
        np.sin(theta1_rad + theta2_rad),
    ])

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], "b-o", linewidth=3, label="Eslabon 1")
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], "r-o", linewidth=3, label="Eslabon 2")
    ax.plot(target_x, target_y, "g*", markersize=15, label="Objetivo (TCP)")
    ax.set_xlim(-l1 - l2 - 1, l1 + l2 + 1)
    ax.set_ylim(-l1 - l2 - 1, l1 + l2 + 1)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.4)
    ax.legend()
    ax.set_title(f"IK: theta1={angulos[0]:.1f} deg | theta2={angulos[1]:.1f} deg")
    plt.tight_layout()
    plt.show()


def main():
    l1, l2 = 10, 10
    target_x, target_y = 5, 10

    angulos, msg = resolver_ik_simple(target_x, target_y, l1, l2)

    if angulos is not None:
        print(f"Resultado: {msg}")
        print(f"  -> Angulo base (theta1): {angulos[0]:.2f} grados")
        print(f"  -> Angulo codo (theta2): {angulos[1]:.2f} grados")
        visualizar_brazo(target_x, target_y, l1, l2, angulos)
    else:
        print(f"Sin solucion: {msg}")


if __name__ == "__main__":
    main()
