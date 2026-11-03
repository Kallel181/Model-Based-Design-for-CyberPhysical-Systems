from dataclasses import dataclass
import json
from pathlib import Path
import numpy as np


@dataclass(frozen=True)
class MotorParameters:
    R_ohm: float
    L_H: float
    Kt_Nm_per_A: float
    Ke_Vs_per_rad: float
    J_kg_m2: float
    b_Nms_per_rad: float
    gear_ratio: float
    V_max_V: float
    i_max_A: float
    sampling_period_s: float
    critical_speed_rad_s: float
    critical_load_torque_Nm: float

    @classmethod
    def from_json(cls, path):
        data = json.loads(
            Path(path).read_text(encoding="utf-8")
        )
        return cls(**data)


def state_space_matrices(p):

    A = np.array([
        [-p.R_ohm / p.L_H,
         -p.Ke_Vs_per_rad / p.L_H],

        [p.Kt_Nm_per_A / p.J_kg_m2,
         -p.b_Nms_per_rad / p.J_kg_m2]
    ])

    B = np.array([
        [1 / p.L_H],
        [0]
    ])

    C = np.array([[0, 1]])

    D = np.array([[0]])

    return A, B, C, D


def state_derivative(x, voltage_V, load_torque_Nm, p):

    current, speed = x

    di_dt = (
        voltage_V
        - p.R_ohm * current
        - p.Ke_Vs_per_rad * speed
    ) / p.L_H

    domega_dt = (
        p.Kt_Nm_per_A * current
        - p.b_Nms_per_rad * speed
        - load_torque_Nm
    ) / p.J_kg_m2

    return np.array([di_dt, domega_dt])


def steady_state_operating_point(p):

    speed = p.critical_speed_rad_s
    torque = p.critical_load_torque_Nm

    current = (
        p.b_Nms_per_rad * speed + torque
    ) / p.Kt_Nm_per_A

    voltage = (
        p.R_ohm * current
        + p.Ke_Vs_per_rad * speed
    )

    return current, voltage

def operating_point_analysis(p):

    speed = p.critical_speed_rad_s
    load = p.critical_load_torque_Nm

    # Corrente necessária em regime permanente
    current = (
        p.b_Nms_per_rad * speed + load
    ) / p.Kt_Nm_per_A

    # Tensão necessária em regime permanente
    voltage = (
        p.R_ohm * current
        + p.Ke_Vs_per_rad * speed
    )

    return {
        "current_A": current,
        "voltage_V": voltage,

        "current_margin_A": (
            p.i_max_A - abs(current)
        ),

        "voltage_margin_V": (
            p.V_max_V - abs(voltage)
        ),

        "current_utilization": (
            abs(current) / p.i_max_A
        ),

        "voltage_utilization": (
            abs(voltage) / p.V_max_V
        )
    }