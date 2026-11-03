from pathlib import Path
import numpy as np

from src.plant.model import MotorParameters
from src.plant.closed_loop import simulate_cascade

ROOT = Path(__file__).resolve().parents[1]


def test_cascade_respects_actuator_limits():

    p = MotorParameters.from_json(
        ROOT / "config" / "motor_parameters.json"
    )

    result = simulate_cascade(
        p,
        reference_deg=90,
        load_torque=0.25,
        duration=1.0
    )

    assert np.max(
        np.abs(result["current_reference"])
    ) <= p.i_max_A + 1e-9

    assert np.max(
        np.abs(result["voltage"])
    ) <= p.V_max_V + 1e-9


def test_simulation_returns_finite_values():

    p = MotorParameters.from_json(
        ROOT / "config" / "motor_parameters.json"
    )

    result = simulate_cascade(p)

    for key in [
        "position",
        "speed",
        "current",
        "voltage"
    ]:
        assert np.all(np.isfinite(result[key]))