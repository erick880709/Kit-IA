"""Pruebas del re-codificado CIE-10 → CIE-11 del vocabulario (2026-08-26)."""

from ml.src.data.mapeo_cie11 import MAPEO_CIE10_A_CIE11, remapear_cie11


def test_catalogo_completo_y_unico() -> None:
    assert len(MAPEO_CIE10_A_CIE11) == 71
    valores = list(MAPEO_CIE10_A_CIE11.values())
    assert len(valores) == len(set(valores)), "códigos CIE-11 duplicados"


def test_remapeo_con_punto() -> None:
    assert remapear_cie11("R10.4") == "DD30"
    assert remapear_cie11("J18.9") == "CA40"
    assert remapear_cie11("I10") == "BA00"
    assert remapear_cie11("R07.4") == "MD30"
    assert remapear_cie11("N39.0") == "GC08"


def test_remapeo_sin_punto_ni_sufijo_x() -> None:
    assert remapear_cie11("R104") == "DD30"
    assert remapear_cie11("J189") == "CA40"
    assert remapear_cie11("R074") == "MD30"
    assert remapear_cie11("K922") == "DB24.B"
    assert remapear_cie11("W349") == "PA80"


def test_codigo_desconocido_pasa_intacto() -> None:
    assert remapear_cie11("Z999") == "Z999"
    assert remapear_cie11("") == ""
    assert remapear_cie11(None) == ""
    assert remapear_cie11("MD30") == "MD30"  # ya CIE-11 → sin cambios


def test_minusculas_y_espacios() -> None:
    assert remapear_cie11("  r10.4 ") == "DD30"
    assert remapear_cie11("a09") == "1A40"
