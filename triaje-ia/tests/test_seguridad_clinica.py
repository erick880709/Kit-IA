"""Pruebas de la red de contención clínica (Res. 5596/2015)."""

from ml.src.models.seguridad_clinica import regla_seguridad_clinica

_PROBAS_NEUTRAS = {"I": 0.05, "II": 0.1, "III": 0.6, "IV": 0.2, "V": 0.05}


def test_spo2_bajo_devuelve_i() -> None:
    assert regla_seguridad_clinica({"saturacion_o2": 84}, _PROBAS_NEUTRAS) == "I"
    assert regla_seguridad_clinica({"saturacion_o2": 85}, _PROBAS_NEUTRAS) is None


def test_presion_sistolica_baja_devuelve_i() -> None:
    assert regla_seguridad_clinica({"presion_sistolica": 69}, _PROBAS_NEUTRAS) == "I"


def test_frecuencia_cardiaca_extrema_devuelve_i() -> None:
    assert regla_seguridad_clinica({"frecuencia_cardiaca": 151}, _PROBAS_NEUTRAS) == "I"
    assert regla_seguridad_clinica({"frecuencia_cardiaca": 39}, _PROBAS_NEUTRAS) == "I"


def test_frecuencia_respiratoria_alta_devuelve_i() -> None:
    assert regla_seguridad_clinica({"frecuencia_respiratoria": 36}, _PROBAS_NEUTRAS) == "I"


def test_glasgow_bajo_devuelve_i() -> None:
    assert regla_seguridad_clinica({"glasgow": 8}, _PROBAS_NEUTRAS) == "I"
    assert regla_seguridad_clinica({"glasgow": 9}, _PROBAS_NEUTRAS) is None


def test_todo_normal_con_pv_devuelve_v() -> None:
    datos = {
        "saturacion_o2": 99, "frecuencia_cardiaca": 70,
        "frecuencia_respiratoria": 14, "temperatura": 36.5,
        "presion_sistolica": 118, "glasgow": 15, "escala_dolor": 1,
    }
    probas = {**_PROBAS_NEUTRAS, "V": 0.25}
    assert regla_seguridad_clinica(datos, probas) == "V"


def test_normal_pero_pv_baja_no_devuelve_v() -> None:
    datos = {
        "saturacion_o2": 99, "frecuencia_cardiaca": 70,
        "frecuencia_respiratoria": 14, "temperatura": 36.5,
        "presion_sistolica": 118, "glasgow": 15, "escala_dolor": 1,
    }
    assert regla_seguridad_clinica(datos, _PROBAS_NEUTRAS) is None  # P(V)=0.05


def test_dolor_alto_no_devuelve_v() -> None:
    datos = {
        "saturacion_o2": 99, "frecuencia_cardiaca": 70,
        "frecuencia_respiratoria": 14, "temperatura": 36.5,
        "presion_sistolica": 118, "glasgow": 15, "escala_dolor": 6,
    }
    assert regla_seguridad_clinica(datos, {**_PROBAS_NEUTRAS, "V": 0.3}) is None


def test_sin_datos_no_rompe() -> None:
    assert regla_seguridad_clinica({}, _PROBAS_NEUTRAS) is None
    assert regla_seguridad_clinica({"saturacion_o2": None}, _PROBAS_NEUTRAS) is None
