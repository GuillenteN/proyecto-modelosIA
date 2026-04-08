#!/usr/bin/env python3

import time

import numpy as np
import torch


ANCHO, ALTO = 1920, 1080
ITERACIONES = 50
KERNEL_SIZE = 21


def main():
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA disponible: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU detectada: {torch.cuda.get_device_name(0)}")

    imagen_np = np.random.randint(0, 255, (ALTO, ANCHO, 3), dtype=np.uint8)
    imagen_tensor = torch.from_numpy(imagen_np).permute(2, 0, 1).unsqueeze(0).float()
    kernel = torch.ones(3, 1, KERNEL_SIZE, KERNEL_SIZE) / (KERNEL_SIZE**2)

    imagen_cpu = imagen_tensor.to("cpu")
    kernel_cpu = kernel.to("cpu")

    tiempos_cpu = []
    for _ in range(ITERACIONES):
        inicio = time.perf_counter()
        _ = torch.nn.functional.conv2d(imagen_cpu, kernel_cpu, padding=KERNEL_SIZE // 2, groups=3)
        tiempos_cpu.append(time.perf_counter() - inicio)

    media_cpu = np.mean(tiempos_cpu)
    print(f"\n[CPU] Tiempo medio: {media_cpu * 1000:.2f} ms | FPS: {1 / media_cpu:.1f}")

    if torch.cuda.is_available():
        imagen_gpu = imagen_tensor.to("cuda")
        kernel_gpu = kernel.to("cuda")

        for _ in range(5):
            _ = torch.nn.functional.conv2d(
                imagen_gpu, kernel_gpu, padding=KERNEL_SIZE // 2, groups=3
            )
        torch.cuda.synchronize()

        tiempos_gpu = []
        for _ in range(ITERACIONES):
            torch.cuda.synchronize()
            inicio = time.perf_counter()
            _ = torch.nn.functional.conv2d(
                imagen_gpu, kernel_gpu, padding=KERNEL_SIZE // 2, groups=3
            )
            torch.cuda.synchronize()
            tiempos_gpu.append(time.perf_counter() - inicio)

        media_gpu = np.mean(tiempos_gpu)
        speedup = media_cpu / media_gpu
        print(f"[GPU] Tiempo medio: {media_gpu * 1000:.2f} ms | FPS: {1 / media_gpu:.1f}")
        print("-" * 40)
        print(f"RESULTADO: La GPU es {speedup:.1f}x mas rapida que la CPU")
    else:
        print("\n[GPU] CUDA no disponible en este entorno.")


if __name__ == "__main__":
    main()
