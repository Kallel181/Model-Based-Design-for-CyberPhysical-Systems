from pathlib import Path

from src.plant.model import MotorParameters
from src.plant.analysis import analyze_plant


ROOT = Path(__file__).resolve().parents[1]


def test_plant_properties():

    p = MotorParameters.from_json(
        ROOT / "config" / "motor_parameters.json"
    )

    result = analyze_plant(p)

    assert result["A"].shape == (2, 2)
    assert result["B"].shape == (2, 1)

    assert result["controllability_rank"] == 2
    assert result["observability_rank"] == 2

    assert all(result["eigenvalues"].real < 0)