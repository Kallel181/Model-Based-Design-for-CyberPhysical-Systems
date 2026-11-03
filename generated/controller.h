#ifndef AURORAARM_CONTROLLER_H
#define AURORAARM_CONTROLLER_H

/*
 * AuroraArm - Generated Controller
 *
 * AUTOMATICALLY GENERATED FILE. DO NOT EDIT.
 *
 * Requirements traceability:
 * CTRL-001: Zero steady-state position error
 * CTRL-002: Overshoot <= 8%
 * CTRL-003: Settling time <= 300 ms
 * CTRL-004: Actuator voltage and current limits
 *
 * Source model: src/codegen/controller_model.py
 * Generation tool: SymPy
 */

typedef struct {
    double position_ref;
    double position;
    double speed;
    double current;

    double kp_pos;
    double ki_pos;
    double kd_pos;

    double kp_current;
    double ki_current;
    double kaw;

    double ts;
    double current_limit;
    double voltage_limit;
} ControllerInput;

typedef struct {
    double position_integral;
    double current_integral;
} ControllerState;

typedef struct {
    double current_ref;
    double voltage;
    double next_position_integral;
    double next_current_integral;
} ControllerOutput;

void auroraarm_controller_step(
    const ControllerInput *input,
    const ControllerState *state,
    ControllerOutput *output
);

#endif
