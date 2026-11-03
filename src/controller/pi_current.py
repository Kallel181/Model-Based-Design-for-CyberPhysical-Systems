class CurrentPI:

    def __init__(
        self,
        kp=0.1508,
        ki=100.531,
        kaw=50.0,
        ts=0.002,
        voltage_limit=48.0
    ):
        self.kp = kp
        self.ki = ki
        self.kaw = kaw
        self.ts = ts

        self.voltage_limit = voltage_limit
        self.integral = 0.0

    def update(self, reference, measured):

        error = reference - measured

        raw_voltage = (
            self.kp * error
            + self.integral
        )

        voltage = max(
            -self.voltage_limit,
            min(self.voltage_limit, raw_voltage)
        )

        # Anti-windup por back-calculation
        self.integral += self.ts * (
            self.ki * error
            + self.kaw * (voltage - raw_voltage)
        )

        return voltage