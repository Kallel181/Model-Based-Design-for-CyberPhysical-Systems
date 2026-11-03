from pathlib import Path
import numpy as np

from src.plant.model import MotorParameters
from src.plant.closed_loop import simulate_cascade
from src.controller.metrics import calculate_metrics

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

metrics = calculate_metrics(
    result["time"],
    result["position"],
    result["reference"]
)

print("\n=== DESEMPENHO DO CONTROLADOR ===")

for name, value in metrics.items():
    print(f"{name}: {value}")

print("\n=== LIMITES FÍSICOS ===")

print(
    "Corrente máxima:",
    np.max(np.abs(result["current"]))
)

print(
    "Tensão máxima:",
    np.max(np.abs(result["voltage"]))
)