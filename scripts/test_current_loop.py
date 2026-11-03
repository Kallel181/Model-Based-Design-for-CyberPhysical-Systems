
import numpy as np
import matplotlib.pyplot as plt

from src.controller.pi_current import CurrentPI


# Parâmetros do experimento
TS = 0.002
DURATION = 0.5
CURRENT_REFERENCE = 4.0

# Parâmetros elétricos do motor
R = 0.8
L = 0.0012

# Discretização exata da dinâmica elétrica:
# di/dt = (V - R*i) / L
a = np.exp(-R * TS / L)
b = (1 - a) / R

# Controlador PI
controller = CurrentPI(
    kp=0.1508,
    ki=100.531,
    kaw=50,
    ts=TS,
    voltage_limit=48
)

# Vetores de simulação
time = np.arange(0, DURATION, TS)
current = np.zeros(len(time))
voltage = np.zeros(len(time))
reference = np.full(len(time), CURRENT_REFERENCE)

# Simulação
for k in range(len(time) - 1):

    voltage[k] = controller.update(
        CURRENT_REFERENCE,
        current[k]
    )

    current[k + 1] = (
        a * current[k]
        + b * voltage[k]
    )

voltage[-1] = voltage[-2]

# Métricas
final_error = abs(CURRENT_REFERENCE - current[-1])

overshoot = max(
    0,
    (np.max(current) - CURRENT_REFERENCE)
    / CURRENT_REFERENCE * 100
)

# Tempo de subida: 10% a 90%
idx_10 = np.where(current >= 0.1 * CURRENT_REFERENCE)[0]
idx_90 = np.where(current >= 0.9 * CURRENT_REFERENCE)[0]

rise_time = (
    time[idx_90[0]] - time[idx_10[0]]
    if len(idx_10) and len(idx_90)
    else float("inf")
)

# Tempo de acomodação: faixa de ±2%
outside = np.where(
    np.abs(current - CURRENT_REFERENCE)
    > 0.02 * CURRENT_REFERENCE
)[0]

settling_time = (
    time[outside[-1] + 1]
    if len(outside) and outside[-1] + 1 < len(time)
    else (0.0 if len(outside) == 0 else float("inf"))
)

print("\n=== TESTE DA MALHA DE CORRENTE ===")
print(f"Erro final: {final_error:.6f} A")
print(f"Sobressinal: {overshoot:.2f}%")
print(f"Tempo de subida: {rise_time:.4f} s")
print(f"Tempo de acomodação: {settling_time:.4f} s")
print(f"Corrente máxima: {np.max(current):.4f} A")
print(f"Tensão máxima: {np.max(np.abs(voltage)):.4f} V")

# Gráficos
fig, axes = plt.subplots(3, 1, figsize=(10, 9))

axes[0].plot(time, reference, "--", label="Referência")
axes[0].plot(time, current, label="Corrente real")
axes[0].set_ylabel("Corrente (A)")
axes[0].set_title("Resposta da malha de corrente")
axes[0].legend()
axes[0].grid()

axes[1].plot(time, voltage)
axes[1].set_ylabel("Tensão (V)")
axes[1].set_title("Tensão aplicada ao motor")
axes[1].grid()

axes[2].plot(time, reference - current)
axes[2].set_ylabel("Erro (A)")
axes[2].set_xlabel("Tempo (s)")
axes[2].set_title("Erro de corrente")
axes[2].grid()

plt.tight_layout()
plt.show()
