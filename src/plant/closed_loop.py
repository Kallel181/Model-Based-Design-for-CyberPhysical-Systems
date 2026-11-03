import numpy as np

from src.plant.discretization import discretize_plant
from src.controller.cascade import CascadeController


def simulate_cascade(
    parameters,
    reference_deg=90.0,
    load_torque=0.25,
    duration=2.0
):

    ts = parameters.sampling_period_s

    controller = CascadeController(parameters)

    Ad, Bd, _, _ = discretize_plant(parameters)

    steps = int(duration / ts) + 1

    time = np.arange(steps) * ts

    # Estados do motor:
    # x[0] = corrente
    # x[1] = velocidade
    x = np.zeros(2)

    # Posição angular do motor
    motor_position = 0.0

    # Referência convertida para radianos da junta
    reference = np.deg2rad(reference_deg)

    ratio = parameters.gear_ratio

    position = np.zeros(steps)
    speed = np.zeros(steps)
    current = np.zeros(steps)
    current_reference = np.zeros(steps)
    voltage = np.zeros(steps)

    for k in range(steps - 1):

        joint_position = motor_position / ratio
        joint_speed = x[1] / ratio

        command = controller.update(
            position_reference=reference,
            joint_position=joint_position,
            joint_speed=joint_speed,
            motor_current=x[0]
        )

        # Entradas: tensão e torque de carga
        u = np.array([
            command["voltage"],
            load_torque
        ])

        # Atualização exata do modelo linear
        x_next = Ad @ x + Bd @ u

        # Integração da posição pelo método trapezoidal
        motor_position += (
            (x[1] + x_next[1]) / 2
        ) * ts

        position[k] = joint_position
        speed[k] = joint_speed
        current[k] = x[0]

        current_reference[k] = command["current_reference"]
        voltage[k] = command["voltage"]

        x = x_next

    position[-1] = motor_position / ratio
    speed[-1] = x[1] / ratio
    current[-1] = x[0]

    current_reference[-1] = current_reference[-2]
    voltage[-1] = voltage[-2]

    return {
        "time": time,
        "position": position,
        "speed": speed,
        "current": current,
        "current_reference": current_reference,
        "voltage": voltage,
        "reference": reference
    }