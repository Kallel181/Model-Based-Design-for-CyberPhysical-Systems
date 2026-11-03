from pathlib import Path
import numpy as np

from src.plant.model import MotorParameters
from src.plant.discretization import discretize_plant

ROOT = Path(__file__).resolve().parents[1]

p = MotorParameters.from_json(
    ROOT / "config" / "motor_parameters.json"
)

Ad, Bd, Cd, Dd = discretize_plant(p)

np.set_printoptions(precision=8, suppress=True)

print("\n=== MODELO DISCRETO ===")

print("\nAd:")
print(Ad)

print("\nBd:")
print(Bd)

print("\nCd:")
print(Cd)

print("\nAutovalores discretos:")
print(np.linalg.eigvals(Ad))