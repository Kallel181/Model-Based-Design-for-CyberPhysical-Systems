import numpy as np
from scipy.integrate import solve_ivp

from src.plant.model import state_derivative


def simulate(parameters, voltage, load_torque=0.0):

    def dynamics(t, z):

        dx = state_derivative(
            z[:2],
            voltage,
            load_torque,
            parameters
        )

        # Posição = integral da velocidade
        return [
            dx[0],
            dx[1],
            z[1]
        ]

    times = np.linspace(0, 0.2, 1001)

    result = solve_ivp(
        dynamics,
        (0, 0.2),
        [0, 0, 0],
        t_eval=times
    )

    return result