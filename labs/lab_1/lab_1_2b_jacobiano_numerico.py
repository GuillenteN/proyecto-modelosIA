#!/usr/bin/env python3

import numpy as np


def cinematica_directa_2d(theta1_deg, theta2_deg, l1, l2):
    t1 = np.radians(theta1_deg)
    t2 = np.radians(theta2_deg)
    x = l1 * np.cos(t1) + l2 * np.cos(t1 + t2)
    y = l1 * np.sin(t1) + l2 * np.sin(t1 + t2)
    return np.array([x, y])


def calcular_jacobiano_numerico(theta1_deg, theta2_deg, l1, l2, delta_deg=0.01):
    delta_rad = np.radians(delta_deg)
    pos_base = cinematica_directa_2d(theta1_deg, theta2_deg, l1, l2)

    pos_pert1 = cinematica_directa_2d(theta1_deg + delta_deg, theta2_deg, l1, l2)
    col1 = (pos_pert1 - pos_base) / delta_rad

    pos_pert2 = cinematica_directa_2d(theta1_deg, theta2_deg + delta_deg, l1, l2)
    col2 = (pos_pert2 - pos_base) / delta_rad

    return np.column_stack([col1, col2])


def main():
    l1, l2 = 10, 10
    t1, t2 = 45.0, 90.0

    pos_tcp = cinematica_directa_2d(t1, t2, l1, l2)
    j = calcular_jacobiano_numerico(t1, t2, l1, l2)

    print(f"Configuracion: theta1={t1} deg, theta2={t2} deg")
    print(f"Posicion TCP:  x={pos_tcp[0]:.4f},  y={pos_tcp[1]:.4f}")
    print("\nMatriz Jacobiana J (numerica):")
    print(f"  [ {j[0,0]:8.4f}  {j[0,1]:8.4f} ]   <- velocidad en X")
    print(f"  [ {j[1,0]:8.4f}  {j[1,1]:8.4f} ]   <- velocidad en Y")

    det_j = np.linalg.det(j)
    print(f"\nDeterminante de J: {det_j:.4f}")
    if abs(det_j) < 0.5:
        print("AVISO: det(J) cercano a 0 -> proximidad a singularidad!")
    else:
        print("OK: Configuracion alejada de singularidades.")

    vel_tcp_deseada = np.array([0.1, 0.0])
    vel_articulaciones = np.linalg.inv(j) @ vel_tcp_deseada
    print(f"\nPara mover el TCP a {vel_tcp_deseada} m/s:")
    print(f"  theta1_dot = {np.degrees(vel_articulaciones[0]):.4f} deg/s")
    print(f"  theta2_dot = {np.degrees(vel_articulaciones[1]):.4f} deg/s")


if __name__ == "__main__":
    main()
