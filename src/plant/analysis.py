import numpy as np

from src.plant.model import (
    state_space_matrices
)


def analyze_plant(parameters):

    A, B, C, D = state_space_matrices(parameters)

    # Autovalores da matriz A
    eigenvalues = np.linalg.eigvals(A)

    # Constantes de tempo
    time_constants = -1 / np.real(eigenvalues)

    # Matriz de controlabilidade
    Wc = np.hstack((B, A @ B))

    # Matriz de observabilidade
    Wo = np.vstack((C, C @ A))

    return {
        "A": A,
        "B": B,
        "C": C,
        "D": D,
        "eigenvalues": eigenvalues,
        "time_constants": time_constants,
        "controllability_rank": np.linalg.matrix_rank(Wc),
        "observability_rank": np.linalg.matrix_rank(Wo)
    }