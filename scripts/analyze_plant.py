from pathlib import Path
import numpy as np

from src.plant.model import MotorParameters
from src.plant.analysis import analyze_plant

ROOT = Path(__file__).resolve().parents[1]

parameters = MotorParameters.from_json(
    ROOT / "config" / "motor_parameters.json"
)

result = analyze_plant(parameters)

np.set_printoptions(precision=6, suppress=True)

print("\n=== MATRIZES DO SISTEMA ===")

print("A:")
print(result["A"])

print("\nB:")
print(result["B"])

print("\nC:")
print(result["C"])

print("\nD:")
print(result["D"])

print("\n=== ANÁLISE DINÂMICA ===")

print("Autovalores:")
print(result["eigenvalues"])

print("\nConstantes de tempo (ms):")
print(result["time_constants"] * 1000)

print("\n=== CONTROLABILIDADE ===")

print(
    result["controllability_rank"],
    "/ 2"
)

print("\n=== OBSERVABILIDADE ===")

print(
    result["observability_rank"],
    "/ 2"
)