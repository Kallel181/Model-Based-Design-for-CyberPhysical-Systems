from pathlib import Path
import numpy as np

from src.plant.model import MotorParameters
from src.plant.discretization import discretize_plant

ROOT = Path(__file__).resolve().parents[1]


def test_discrete_model():

    p = MotorParameters.from_json(
        ROOT / "config" / "motor_parameters.json"
    )

    Ad, Bd, Cd, Dd = discretize_plant(p)

    assert Ad.shape == (2, 2)
    assert Bd.shape == (2, 2)

    assert np.all(
        np.abs(np.linalg.eigvals(Ad)) < 1
    )

    assert np.allclose(
        Ad,
        [[0.25124846, -0.07748468],
         [0.22138481, 0.98012539]],
        atol=1e-6
    )