#!/usr/bin/env python3

reglas_diagnostico = {
    "Fallo_Sistema": ["Fallo_Alimentacion", "Fallo_Software"],
    "Fallo_Alimentacion": ["Bateria_Vacia", "Cable_Desconectado"],
    "Fallo_Software": ["Error_Kernel", "Proceso_ROS_Caido"],
}

hechos_reales = {"Proceso_ROS_Caido"}
cadena_razonamiento = []


def verificar_meta(meta, profundidad=0):
    sangria = "  " * profundidad
    cadena_razonamiento.append(f"{sangria}Verificando: '{meta}'")

    if meta in hechos_reales:
        cadena_razonamiento.append(f"{sangria}  -> VERDADERO (Hecho observado)")
        return True

    if meta in reglas_diagnostico:
        for sub_meta in reglas_diagnostico[meta]:
            if verificar_meta(sub_meta, profundidad + 1):
                cadena_razonamiento.append(
                    f"{sangria}  -> VERDADERO (probado via '{sub_meta}')"
                )
                return True

    cadena_razonamiento.append(f"{sangria}  -> FALSO (no se puede probar)")
    return False


def main():
    objetivo = "Fallo_Sistema"
    print("=== Diagnostico por Backward Chaining ===")
    print(f"Hechos observados: {hechos_reales}\n")
    print("--- Cadena de razonamiento ---")

    resultado = verificar_meta(objetivo)

    for linea in cadena_razonamiento:
        print(linea)

    estado = "CONFIRMADO" if resultado else "NO CONFIRMADO"
    print(f"\n=== RESULTADO: '{objetivo}' es {estado} ===")


if __name__ == "__main__":
    main()
