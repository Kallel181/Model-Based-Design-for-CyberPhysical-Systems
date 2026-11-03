from src.controller.pid_position import PositionPID
from src.controller.pi_current import CurrentPI


class CascadeController:

    def __init__(self, parameters):

        self.position_controller = PositionPID(
            ts=parameters.sampling_period_s,
            current_limit=parameters.i_max_A
        )

        self.current_controller = CurrentPI(
            ts=parameters.sampling_period_s,
            voltage_limit=parameters.V_max_V
        )

    def update(
        self,
        position_reference,
        joint_position,
        joint_speed,
        motor_current
    ):

        # Malha externa:
        # Posição -> corrente de referência
        current_reference = self.position_controller.update(
            position_reference,
            joint_position,
            joint_speed
        )

        # Malha interna:
        # Corrente -> tensão
        voltage = self.current_controller.update(
            current_reference,
            motor_current
        )

        return {
            "current_reference": current_reference,
            "voltage": voltage
        }