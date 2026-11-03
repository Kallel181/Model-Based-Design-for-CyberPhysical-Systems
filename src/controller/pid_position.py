class PositionPID:

    def __init__(
        self,
        kp=12.0,
        ki=3.0,
        kd=2.0,
        ts=0.002,
        current_limit=8.0
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.ts = ts

        self.current_limit = current_limit
        self.integral = 0.0

    def update(self, reference, position, speed):

        error = reference - position

        # Derivada sobre a medição
        derivative_term = -self.kd * speed

        # Calcula a saída antes da saturação
        raw_output = (
            self.kp * error
            + self.integral
            + derivative_term
        )

        output = max(
            -self.current_limit,
            min(self.current_limit, raw_output)
        )

        # Integra somente quando não agrava a saturação
        if (
            abs(raw_output) <= self.current_limit
            or error * raw_output <= 0
        ):
            self.integral += self.ki * error * self.ts

        return output