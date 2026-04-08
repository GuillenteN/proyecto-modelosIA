#!/usr/bin/env python3


class SistemaExpertoSalud:
    def __init__(self):
        self.memoria_hechos = {}
        self.telemetria = {}
        self.diagnosticos = []

    def actualizar_hechos(self, telemetria):
        self.telemetria = telemetria
        self.memoria_hechos["v_bajo"] = telemetria["voltaje"] < 11.0
        self.memoria_hechos["temp_alta"] = telemetria["temperatura"] > 85.0
        self.memoria_hechos["perdida_paquetes"] = telemetria["latencia"] > 100
        self.memoria_hechos["corriente_alta"] = telemetria["amperaje"] > 5.0

    def inferir(self):
        self.diagnosticos = []
        t = self.telemetria

        if self.memoria_hechos["v_bajo"] and self.memoria_hechos["corriente_alta"]:
            self.diagnosticos.append(
                {
                    "nivel": "FALLO CRITICO",
                    "mensaje": "Posible cortocircuito en celdas de bateria.",
                    "evidencia": [
                        f"Voltaje ({t['voltaje']}V < 11.0V)",
                        f"Amperaje ({t['amperaje']}A > 5.0A)",
                    ],
                    "no_cumplidas": [
                        k
                        for k, v in self.memoria_hechos.items()
                        if not v and k not in ["v_bajo", "corriente_alta"]
                    ],
                }
            )

        if self.memoria_hechos["temp_alta"] and self.memoria_hechos["corriente_alta"]:
            self.diagnosticos.append(
                {
                    "nivel": "MANTENIMIENTO",
                    "mensaje": "Esfuerzo mecanico excesivo en articulaciones.",
                    "evidencia": [
                        f"Temperatura ({t['temperatura']}C > 85.0C)",
                        f"Amperaje ({t['amperaje']}A > 5.0A)",
                    ],
                    "no_cumplidas": [
                        k
                        for k, v in self.memoria_hechos.items()
                        if not v and k not in ["temp_alta", "corriente_alta"]
                    ],
                }
            )

        if self.memoria_hechos["perdida_paquetes"] and self.memoria_hechos["temp_alta"]:
            self.diagnosticos.append(
                {
                    "nivel": "FALLO LOGICO",
                    "mensaje": "Throttling en Jetson por temperatura excesiva.",
                    "evidencia": [
                        f"Latencia ({t['latencia']}ms > 100ms)",
                        f"Temperatura ({t['temperatura']}C > 85.0C)",
                    ],
                    "no_cumplidas": [
                        k
                        for k, v in self.memoria_hechos.items()
                        if not v and k not in ["perdida_paquetes", "temp_alta"]
                    ],
                }
            )

        return self.diagnosticos


def main():
    log_robot = {
        "voltaje": 10.5,
        "temperatura": 92.0,
        "latencia": 120,
        "amperaje": 6.2,
    }

    se = SistemaExpertoSalud()
    se.actualizar_hechos(log_robot)
    alertas = se.inferir()

    print("=" * 50)
    print("   REPORTE DEL SISTEMA EXPERTO DE SALUD")
    print("=" * 50)
    print(f"Telemetria recibida: {log_robot}\n")

    if not alertas:
        print("[OK] Sistema en estado nominal. Sin alertas.")
    else:
        for diag in alertas:
            print(f"[{diag['nivel']}] {diag['mensaje']}")
            print(f"  Evidencia positiva: {' Y '.join(diag['evidencia'])}")
            if diag["no_cumplidas"]:
                print(f"  Condiciones NO cumplidas en esta regla: {diag['no_cumplidas']}")
            print()


if __name__ == "__main__":
    main()
