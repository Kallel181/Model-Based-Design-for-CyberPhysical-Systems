import numpy as np
from scipy.signal import cont2discrete

from src.plant.model import state_space_matrices


def discretize_plant(p):

    A, B, C, D = state_space_matrices(p)

    # Segunda entrada: torque de carga
    B_aug = np.array([
        [1 / p.L_H, 0],
        [0, -1 / p.J_kg_m2]
    ])

    D_aug = np.zeros((1, 2))

    Ad, Bd, Cd, Dd, dt = cont2discrete(
        (A, B_aug, C, D_aug),
        p.sampling_period_s,
        method="zoh"
    )

    return Ad, Bd, Cd, Dd