"""Pruebas del re-codificado CIE-10 → CIE-11 del vocabulario (2026-08-26)."""

from ml.src.data.mapeo_cie11 import (
    MAPEO_CIE10_A_CIE11,
    normalizar_token_cie,
    remapear_cie11,
)


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


def test_normalizar_token_cie_unico_y_estable() -> None:
    # Códigos con punto NO colisionan tras normalizar
    assert normalizar_token_cie("MF50.7") == "MF507"
    assert normalizar_token_cie("MF50.4") == "MF504"
    assert normalizar_token_cie("DB24.B") == "DB24B"
    assert normalizar_token_cie("MD81.3") == "MD813"
    assert normalizar_token_cie("ME84.2") == "ME842"
    # Sin punto: estables
    assert normalizar_token_cie("8A8Z") == "8A8Z"
    assert normalizar_token_cie("1A40") == "1A40"
    assert normalizar_token_cie("DD30") == "DD30"
    assert normalizar_token_cie(None) == ""
    assert normalizar_token_cie("") == ""


def test_todos_los_tokens_normalizados_son_unicos() -> None:
    from app.domain.catalogos import CATALOGO_MOTIVOS

    tokens = [normalizar_token_cie(c) for c, _, _ in CATALOGO_MOTIVOS]
    assert len(tokens) == len(set(tokens)), "tokens CIE-11 normalizados duplicados"
    assert all(t for t in tokens)
