from pathlib import Path
import matplotlib.pyplot as plt

from src.plant.model import MotorParameters
from src.plant.simulation import simulate

ROOT = Path(__file__).resolve().parents[1]

p = MotorParameters.from_json(
    ROOT / "config" / "motor_parameters.json"
)

result = simulate(
    p,
    voltage=10,
    load_torque=0
)

time = result.t * 1000

fig, axes = plt.subplots(3, 1, figsize=(9, 8))

axes[0].plot(time, result.y[0])
axes[0].set_ylabel("Corrente (A)")

axes[1].plot(time, result.y[1])
axes[1].set_ylabel("Velocidade (rad/s)")

axes[2].plot(time, result.y[2])
axes[2].set_ylabel("Posição (rad)")
axes[2].set_xlabel("Tempo (ms)")

for ax in axes:
    ax.grid()

plt.tight_layout()
plt.show()