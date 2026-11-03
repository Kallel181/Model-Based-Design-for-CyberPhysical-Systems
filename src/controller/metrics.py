
import numpy as np


def calculate_metrics(time, position, reference):

    error = reference - position

    final_error = abs(error[-1])

    overshoot = max(
        0.0,
        (np.max(position) - reference)
        / abs(reference) * 100
    )

    tolerance = 0.02 * abs(reference)

    outside = np.where(
        np.abs(error) > tolerance
    )[0]

    if len(outside) == 0:
        settling_time = 0.0

    elif outside[-1] == len(time) - 1:
        settling_time = float("inf")

    else:
        settling_time = time[outside[-1] + 1]

    return {
        "final_error_rad": final_error,
        "overshoot_percent": overshoot,
        "settling_time_s": settling_time
    }
