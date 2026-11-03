#include "controller.h"
#include <math.h>

void auroraarm_controller_step(
    const ControllerInput *input,
    const ControllerState *state,
    ControllerOutput *output
) {
    const double position_ref = input->position_ref;
    const double position = input->position;
    const double speed = input->speed;
    const double current = input->current;
    const double kp_pos = input->kp_pos;
    const double ki_pos = input->ki_pos;
    const double kd_pos = input->kd_pos;
    const double kp_current = input->kp_current;
    const double ki_current = input->ki_current;
    const double kaw = input->kaw;
    const double ts = input->ts;
    const double current_limit = input->current_limit;
    const double voltage_limit = input->voltage_limit;
    const double position_integral = state->position_integral;
    const double current_integral = state->current_integral;

    if (current_limit < -kd_pos*speed + kp_pos*(-position + position_ref) + position_integral) {
       output->current_ref = current_limit;
    }
    else if (current_limit < kd_pos*speed - kp_pos*(-position + position_ref) - position_integral) {
       output->current_ref = -current_limit;
    }
    else {
       output->current_ref = -kd_pos*speed + kp_pos*(-position + position_ref) + position_integral;
    }

    if (((current_limit < -kd_pos*speed + kp_pos*(-position + position_ref) + position_integral) ? (
       voltage_limit < current_integral + kp_current*(-current + current_limit)
    )
    : (
       ((current_limit < kd_pos*speed - kp_pos*(-position + position_ref) - position_integral) ? (
          voltage_limit < current_integral + kp_current*(-current - current_limit)
       )
       : (
          voltage_limit < current_integral + kp_current*(-current - kd_pos*speed + kp_pos*(-position + position_ref) + position_integral)
       ))
    ))) {
       output->voltage = voltage_limit;
    }
    else if (((current_limit < -kd_pos*speed + kp_pos*(-position + position_ref) + position_integral) ? (
       voltage_limit < -current_integral - kp_current*(-current + current_limit)
    )
    : (
       ((current_limit < kd_pos*speed - kp_pos*(-position + position_ref) - position_integral) ? (
          voltage_limit < -current_integral - kp_current*(-current - current_limit)
       )
       : (
          voltage_limit < -current_integral - kp_current*(-current - kd_pos*speed + kp_pos*(-position + position_ref) + position_integral)
       ))
    ))) {
       output->voltage = -voltage_limit;
    }
    else {
       output->voltage = current_integral + kp_current*(-current + ((current_limit < -kd_pos*speed + kp_pos*(-position + position_ref) + position_integral) ? (
          current_limit
       )
       : ((current_limit < kd_pos*speed - kp_pos*(-position + position_ref) - position_integral) ? (
          -current_limit
       )
       : (
          -kd_pos*speed + kp_pos*(-position + position_ref) + position_integral
       ))));
    }

    if (current_limit >= fabs(kd_pos*speed + kp_pos*(position - position_ref) - position_integral) || (-position + position_ref)*(-kd_pos*speed + kp_pos*(-position + position_ref) + position_integral) <= 0) {
       output->next_position_integral = ki_pos*ts*(-position + position_ref) + position_integral;
    }
    else {
       output->next_position_integral = position_integral;
    }

    output->next_current_integral = current_integral + ts*(kaw*(-current_integral - kp_current*(-current + ((current_limit < -kd_pos*speed + kp_pos*(-position + position_ref) + position_integral) ? (
       current_limit
    )
    : ((current_limit < kd_pos*speed - kp_pos*(-position + position_ref) - position_integral) ? (
       -current_limit
    )
    : (
       -kd_pos*speed + kp_pos*(-position + position_ref) + position_integral
    )))) + ((((current_limit < -kd_pos*speed + kp_pos*(-position + position_ref) + position_integral) ? (
       voltage_limit < current_integral + kp_current*(-current + current_limit)
    )
    : (
       ((current_limit < kd_pos*speed - kp_pos*(-position + position_ref) - position_integral) ? (
          voltage_limit < current_integral + kp_current*(-current - current_limit)
       )
       : (
          voltage_limit < current_integral + kp_current*(-current - kd_pos*speed + kp_pos*(-position + position_ref) + position_integral)
       ))
    ))) ? (
       voltage_limit
    )
    : ((((current_limit < -kd_pos*speed + kp_pos*(-position + position_ref) + position_integral) ? (
       voltage_limit < -current_integral - kp_current*(-current + current_limit)
    )
    : (
       ((current_limit < kd_pos*speed - kp_pos*(-position + position_ref) - position_integral) ? (
          voltage_limit < -current_integral - kp_current*(-current - current_limit)
       )
       : (
          voltage_limit < -current_integral - kp_current*(-current - kd_pos*speed + kp_pos*(-position + position_ref) + position_integral)
       ))
    ))) ? (
       -voltage_limit
    )
    : (
       current_integral + kp_current*(-current + ((current_limit < -kd_pos*speed + kp_pos*(-position + position_ref) + position_integral) ? (
          current_limit
       )
       : ((current_limit < kd_pos*speed - kp_pos*(-position + position_ref) - position_integral) ? (
          -current_limit
       )
       : (
          -kd_pos*speed + kp_pos*(-position + position_ref) + position_integral
       ))))
    )))) + ki_current*(-current + ((current_limit < -kd_pos*speed + kp_pos*(-position + position_ref) + position_integral) ? (
       current_limit
    )
    : ((current_limit < kd_pos*speed - kp_pos*(-position + position_ref) - position_integral) ? (
       -current_limit
    )
    : (
       -kd_pos*speed + kp_pos*(-position + position_ref) + position_integral
    )))));

}
