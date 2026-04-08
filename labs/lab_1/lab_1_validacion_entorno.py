#!/usr/bin/env python3

import subprocess
import sys


print("=" * 50)
print("  VALIDACION DEL ENTORNO DE SIMULACION")
print("=" * 50)

print(f"\n[1/4] Python: {sys.version.split()[0]}  OK")

# En ejecuciones no interactivas (como docker run ... python3 script.py),
# el entorno de ROS puede no estar en PATH aunque exista en /opt/ros/humble.
resultado = subprocess.run(
    ["bash", "-lc", "source /opt/ros/humble/setup.bash && ros2 --help >/dev/null"],
    capture_output=True,
    text=True,
)
if resultado.returncode == 0:
    print("[2/4] ROS 2:  entorno ROS 2 cargado correctamente  OK")
else:
    print("[2/4] ROS 2:  ERROR - no se encuentra el ejecutable ros2")
    print("      Asegurate de haber ejecutado:")
    print("      source /opt/ros/humble/setup.bash")

librerias = ["numpy", "matplotlib", "pybullet", "skfuzzy"]
for lib in librerias:
    try:
        __import__(lib)
        print(f"[3/4] {lib:<15}  OK")
    except ImportError:
        print(f"[3/4] {lib:<15}  ERROR - ejecuta: pip install {lib}")

print("\n[4/4] Ejecutando simulacion de prueba con PyBullet...")
try:
    import pybullet as p
    import pybullet_data

    p.connect(p.DIRECT)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)

    robot_id = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0])
    num_joints = p.getNumJoints(robot_id)
    print(f"      Robot KUKA cargado. Articulaciones detectadas: {num_joints}")

    objetivo_rad = 0.785
    p.setJointMotorControl2(
        bodyIndex=robot_id,
        jointIndex=0,
        controlMode=p.POSITION_CONTROL,
        targetPosition=objetivo_rad,
    )

    for _ in range(240):
        p.stepSimulation()

    estado = p.getJointState(robot_id, 0)
    posicion_final_deg = estado[0] * 180 / 3.14159
    error_deg = abs(posicion_final_deg - 45.0)

    if error_deg < 1.0:
        print(f"      Articulacion 0: {posicion_final_deg:.2f} grados  OK")
    else:
        print(f"      AVISO: posicion esperada 45 deg, obtenida {posicion_final_deg:.2f} deg")

    p.disconnect()

except Exception as e:
    print(f"      ERROR en PyBullet: {e}")

print("\n" + "=" * 50)
print("  Si todos los tests muestran OK, el entorno")
print("  esta listo para los siguientes capitulos.")
print("=" * 50)
