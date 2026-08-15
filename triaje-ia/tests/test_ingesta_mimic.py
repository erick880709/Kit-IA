"""Pruebas del adaptador local de MIMIC-IV-ED (ingesta sin red)."""

from __future__ import annotations

import pandas as pd

from ml.src.data.ingesta import ingestar_mimic_ed


def _escribir_fixtures(tmp_path) -> None:
    pd.DataFrame(
        {
            "subject_id": [1, 2, 3],
            "stay_id": [101, 102, 103],
            "temperature": [36.5, 38.9, 37.0],
            "heartrate": [80, 121, 70],
            "resprate": [16, 30, 14],
            "o2sat": [98, 86, 99],
            "sbp": [120, 98, 130],
            "dbp": [80, 62, 85],
            "pain": [2, 8, 0],
            "acuity": [3, 1, 5],
            "chiefcomplaint": ["dolor abdominal", "herida por arma de fuego", "tos"],
        }
    ).to_csv(tmp_path / "triage.csv", index=False)
    pd.DataFrame(
        {
            "subject_id": [1, 2, 3],
            "hadm_id": [pd.NA] * 3,
            "stay_id": [101, 102, 103],
            "intime": ["2020-01-01 08:00"] * 3,
            "outtime": ["2020-01-01 10:00"] * 3,
            "gender": ["F", "M", "F"],
            "race": ["WHITE"] * 3,
            "arrival_transport": ["WALK IN", "AMBULANCE", "UNKNOWN"],
            "disposition": ["HOME", "ADMITTED", "HOME"],
        }
    ).to_csv(tmp_path / "edstays.csv", index=False)
    pd.DataFrame(
        {
            "subject_id": [1, 2, 3],
            "stay_id": [101, 102, 103],
            "seq_num": [1, 1, 1],
            "icd_code": ["R104", "W349", "R05"],
            "icd_version": [10, 10, 10],
            "icd_title": ["Dolor abdominal", "Herida arma fuego", "Tos"],
        }
    ).to_csv(tmp_path / "diagnosis.csv", index=False)


def test_ingesta_mimic_mapea_acuity_y_transporte(tmp_path) -> None:
    _escribir_fixtures(tmp_path)
    df = ingestar_mimic_ed(tmp_path)
    assert len(df) == 3
    assert df.loc[1, "nivel_triaje"] == "I"  # acuity 1 → I
    assert df.loc[0, "nivel_triaje"] == "III"
    assert df.loc[1, "via_llegada"] == "Ambulancia"
    assert df.loc[0, "via_llegada"] == "Particular"
    assert df.loc[1, "motivo_codigo_cie10"] == "W349"
    assert df.loc[1, "motivo_texto"] == "herida por arma de fuego"
    assert (df["fuente"] == "mimic-iv-ed").all()


def test_ingesta_mimic_descarta_acuity_invalida(tmp_path) -> None:
    _escribir_fixtures(tmp_path)
    triage = pd.read_csv(tmp_path / "triage.csv")
    triage.loc[2, "acuity"] = 9
    triage.to_csv(tmp_path / "triage.csv", index=False)
    df = ingestar_mimic_ed(tmp_path)
    assert len(df) == 2
