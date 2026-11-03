
import ctypes
import subprocess
from pathlib import Path

import numpy as np
import sympy as sp

from src.codegen.controller_model import build_controller_model


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated"
DLL_PATH = GENERATED / "controller.dll"


# --------------------------------------------------
# 1. Compilar o código C como biblioteca compartilhada
# --------------------------------------------------

subprocess.run(
    [
        "gcc",
        "-std=c99",
        "-shared",
        "-O2",
        "-o",
        str(DLL_PATH),
        str(GENERATED / "controller.c"),
    ],
    check=True,
)

print("Biblioteca C compilada.")


# --------------------------------------------------
# 2. Definir estruturas compatíveis com o C
# --------------------------------------------------

class ControllerInput(ctypes.Structure):
    _fields_ = [
        ("position_ref", ctypes.c_double),
        ("position", ctypes.c_double),
        ("speed", ctypes.c_double),
        ("current", ctypes.c_double),
        ("kp_pos", ctypes.c_double),
        ("ki_pos", ctypes.c_double),
        ("kd_pos", ctypes.c_double),
        ("kp_current", ctypes.c_double),
        ("ki_current", ctypes.c_double),
        ("kaw", ctypes.c_double),
        ("ts", ctypes.c_double),
        ("current_limit", ctypes.c_double),
        ("voltage_limit", ctypes.c_double),
    ]


class ControllerState(ctypes.Structure):
    _fields_ = [
        ("position_integral", ctypes.c_double),
        ("current_integral", ctypes.c_double),
    ]


class ControllerOutput(ctypes.Structure):
    _fields_ = [
        ("current_ref", ctypes.c_double),
        ("voltage", ctypes.c_double),
        ("next_position_integral", ctypes.c_double),
        ("next_current_integral", ctypes.c_double),
    ]


# --------------------------------------------------
# 3. Carregar a função C
# --------------------------------------------------

library = ctypes.CDLL(str(DLL_PATH))

c_step = library.auroraarm_controller_step

c_step.argtypes = [
    ctypes.POINTER(ControllerInput),
    ctypes.POINTER(ControllerState),
    ctypes.POINTER(ControllerOutput),
]

c_step.restype = None


# --------------------------------------------------
# 4. Preparar modelo simbólico de referência
# --------------------------------------------------

model = build_controller_model()

symbols = {
    symbol.name: symbol
    for expression in model.values()
    for symbol in expression.free_symbols
}

symbol_order = [
    "position_ref",
    "position",
    "speed",
    "current",
    "position_integral",
    "current_integral",
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

ordered_symbols = [
    symbols[name] for name in symbol_order
]

reference_functions = {
    name: sp.lambdify(
        ordered_symbols,
        model[name],
        modules="math"
    )
    for name in (
        "current_ref",
        "voltage",
        "next_position_integral",
        "next_current_integral",
    )
}


# --------------------------------------------------
# 5. Parâmetros do experimento
# --------------------------------------------------

params = {
    "kp_pos": 12.0,
    "ki_pos": 3.0,
    "kd_pos": 2.0,
    "kp_current": 0.1508,
    "ki_current": 100.531,
    "kaw": 50.0,
    "ts": 0.002,
    "current_limit": 8.0,
    "voltage_limit": 48.0,
}

state_python = {
    "position_integral": 0.0,
    "current_integral": 0.0,
}

state_c = ControllerState(0.0, 0.0)

max_difference = 0.0
samples = 2000


# --------------------------------------------------
# 6. Executar comparação ciclo a ciclo
# --------------------------------------------------

for k in range(samples):

    t = k * params["ts"]

    inputs = {
        "position_ref": 1.5708,
        "position": 1.5708 * (1 - np.exp(-2 * t)),
        "speed": 0.8 * np.exp(-2 * t),
        "current": 3.5 * (1 - np.exp(-5 * t)),
        **params,
    }

    values = {
        **inputs,
        **state_python,
    }

    args = [
        values[name]
        for name in symbol_order
    ]

    # Referência simbólica Python
    reference = {
        name: float(function(*args))
        for name, function in reference_functions.items()
    }

    # Execução do código C
    c_input = ControllerInput(
        **inputs
    )

    c_output = ControllerOutput()

    c_step(
        ctypes.byref(c_input),
        ctypes.byref(state_c),
        ctypes.byref(c_output),
    )

    c_values = {
        "current_ref": c_output.current_ref,
        "voltage": c_output.voltage,
        "next_position_integral": c_output.next_position_integral,
        "next_current_integral": c_output.next_current_integral,
    }

    # Comparar todas as saídas
    for name in reference:

        difference = abs(
            reference[name] - c_values[name]
        )

        max_difference = max(
            max_difference,
            difference
        )

    # Atualizar estados independentemente
    state_python["position_integral"] = (
        reference["next_position_integral"]
    )

    state_python["current_integral"] = (
        reference["next_current_integral"]
    )

    state_c.position_integral = (
        c_output.next_position_integral
    )

    state_c.current_integral = (
        c_output.next_current_integral
    )


# --------------------------------------------------
# 7. Resultado
# --------------------------------------------------

tolerance = 1e-9

print("\n=== TESTE SOFTWARE-IN-THE-LOOP ===")
print(f"Ciclos executados: {samples}")
print(f"Maior diferença: {max_difference:.12e}")
print(f"Tolerância: {tolerance:.1e}")

if max_difference <= tolerance:
    print("RESULTADO: APROVADO")
else:
    print("RESULTADO: REPROVADO")
    raise AssertionError(
        "Diferença entre modelo Python e código C."
    )
