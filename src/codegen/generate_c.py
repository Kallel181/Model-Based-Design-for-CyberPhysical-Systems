
from pathlib import Path
import sympy as sp

from src.codegen.controller_model import build_controller_model


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "generated"

INPUT_FIELDS = [
    "position_ref",
    "position",
    "speed",
    "current",
    "kp_pos",
    "ki_pos",
    "kd_pos",
    "kp_current",
    "ki_current",
    "kaw",
    "ts",
    "current_limit",
    "voltage_limit",
]

STATE_FIELDS = [
    "position_integral",
    "current_integral",
]

OUTPUT_FIELDS = [
    "current_ref",
    "voltage",
    "next_position_integral",
    "next_current_integral",
]


def generate_header():
    return """\
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
"""


def generate_source(model):
    lines = [
        '#include "controller.h"',
        "#include <math.h>",
        "",
        "void auroraarm_controller_step(",
        "    const ControllerInput *input,",
        "    const ControllerState *state,",
        "    ControllerOutput *output",
        ") {",
    ]

    # Mapear os símbolos matemáticos para os campos das estruturas C.
    for field in INPUT_FIELDS:
        lines.append(
            f"    const double {field} = input->{field};"
        )

    for field in STATE_FIELDS:
        lines.append(
            f"    const double {field} = state->{field};"
        )

    lines.append("")

    # Gerar as atribuições C diretamente das expressões SymPy.
    for name in OUTPUT_FIELDS:
        expression = model[name]

        generated_code = sp.ccode(
            expression,
            assign_to=f"output->{name}"
        )

        for line in generated_code.splitlines():
            lines.append(f"    {line}")

        lines.append("")

    lines.append("}")

    return "\n".join(lines) + "\n"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    model = build_controller_model()

    header = generate_header()
    source = generate_source(model)

    header_path = OUTPUT_DIR / "controller.h"
    source_path = OUTPUT_DIR / "controller.c"

    header_path.write_text(header, encoding="utf-8")
    source_path.write_text(source, encoding="utf-8")

    print("=== GERAÇÃO DE C CONCLUÍDA ===")
    print(f"Header: {header_path}")
    print(f"Source: {source_path}")


if __name__ == "__main__":
    main()
