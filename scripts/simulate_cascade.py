from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from src.plant.model import MotorParameters
from src.plant.closed_loop import simulate_cascade

ROOT = Path(__file__).resolve().parents[1]

p = MotorParameters.from_json(
    ROOT / "config" / "motor_parameters.json"
)

result = simulate_cascade(
    p,
    reference_deg=90,
    load_torque=0.25,
    duration=10.0
)

time = result["time"]

fig, axes = plt.subplots(4, 1, figsize=(10, 11))

axes[0].plot(
    time,
    np.rad2deg(result["position"])
)
axes[0].axhline(90, linestyle="--")
axes[0].set_ylabel("Posição da junta (°)")

axes[1].plot(
    time,
    result["current"],
    label="Corrente real"
)
axes[1].plot(
    time,
    result["current_reference"],
    linestyle="--",
    label="Corrente desejada"
)
axes[1].set_ylabel("Corrente (A)")
axes[1].legend()

axes[2].plot(
    time,
    result["voltage"]
)
axes[2].set_ylabel("Tensão (V)")

axes[3].plot(
    time,
    result["speed"]
)
axes[3].set_ylabel("Velocidade (rad/s)")
axes[3].set_xlabel("Tempo (s)")

for ax in axes:
    ax.grid()

plt.tight_layout()
plt.show()