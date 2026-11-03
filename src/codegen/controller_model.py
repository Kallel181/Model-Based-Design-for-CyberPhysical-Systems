
import sympy as sp


def build_controller_model():

    # Entradas
    position_ref = sp.Symbol("position_ref")
    position = sp.Symbol("position")
    speed = sp.Symbol("speed")
    current = sp.Symbol("current")

    # Estados internos
    position_integral = sp.Symbol("position_integral")
    current_integral = sp.Symbol("current_integral")

    # Parâmetros do PID externo
    kp_pos = sp.Symbol("kp_pos")
    ki_pos = sp.Symbol("ki_pos")
    kd_pos = sp.Symbol("kd_pos")

    # Parâmetros do PI interno
    kp_current = sp.Symbol("kp_current")
    ki_current = sp.Symbol("ki_current")
    kaw = sp.Symbol("kaw")

    # Parâmetros gerais
    ts = sp.Symbol("ts")
    current_limit = sp.Symbol("current_limit")
    voltage_limit = sp.Symbol("voltage_limit")

    # PID de posição
    position_error = position_ref - position

    raw_current_ref = (
        kp_pos * position_error
        + position_integral
        - kd_pos * speed
    )

    current_ref = sp.Piecewise(
        (current_limit, raw_current_ref > current_limit),
        (-current_limit, raw_current_ref < -current_limit),
        (raw_current_ref, True)
    )

    # Anti-windup do PID de posição
    integrate_position = sp.Or(
        sp.Abs(raw_current_ref) <= current_limit,
        position_error * raw_current_ref <= 0
    )

    next_position_integral = sp.Piecewise(
        (
            position_integral + ki_pos * position_error * ts,
            integrate_position
        ),
        (position_integral, True)
    )

    # PI de corrente
    current_error = current_ref - current

    raw_voltage = (
        kp_current * current_error
        + current_integral
    )

    voltage = sp.Piecewise(
        (voltage_limit, raw_voltage > voltage_limit),
        (-voltage_limit, raw_voltage < -voltage_limit),
        (raw_voltage, True)
    )

    # Anti-windup por back-calculation
    next_current_integral = (
        current_integral
        + ts * (
            ki_current * current_error
            + kaw * (voltage - raw_voltage)
        )
    )

    return {
        "position_error": position_error,
        "raw_current_ref": raw_current_ref,
        "current_ref": current_ref,
        "next_position_integral": next_position_integral,
        "current_error": current_error,
        "raw_voltage": raw_voltage,
        "voltage": voltage,
        "next_current_integral": next_current_integral,
    }


if __name__ == "__main__":

    model = build_controller_model()

    print("=== MODELO SIMBÓLICO DO CONTROLADOR ===")

    for name, expression in model.items():
        print(f"\n{name}:")
        print(sp.pretty(expression))
