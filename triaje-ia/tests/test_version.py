"""Tests del marcador de versión desplegable (2026-08-27)."""

from __future__ import annotations

import subprocess

from app.version import version_app


def test_version_app_devuelve_cadena_estable() -> None:
    version = version_app()
    assert isinstance(version, str) and version
    assert version.startswith("build ")


def test_version_app_fallback_sin_git(monkeypatch) -> None:
    def _sin_git(*_args, **_kwargs):
        raise OSError("git no disponible")

    monkeypatch.setattr(subprocess, "run", _sin_git)
    assert version_app() == "build local"


def test_version_app_fallback_git_falla(monkeypatch) -> None:
    class _Resultado:
        returncode = 128
        stdout = ""

    monkeypatch.setattr(subprocess, "run", lambda *_a, **_k: _Resultado())
    assert version_app() == "build local"
