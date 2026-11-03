from pathlib import Path

from src.plant.model import (
    MotorParameters,
    operating_point_analysis
)

ROOT = Path(__file__).resolve().parents[1]

p = MotorParameters.from_json(
    ROOT / "config" / "motor_parameters.json"
)

result = operating_point_analysis(p)

print("\n=== PONTO DE OPERAÇÃO CRÍTICO ===")

for name, value in result.items():
    print(f"{name}: {value:.6f}")