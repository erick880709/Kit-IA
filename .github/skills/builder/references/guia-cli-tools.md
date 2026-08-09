# Guía: Desarrollo de CLI Tools

Patrones y stacks recomendados para construir herramientas de línea de comandos (CLI) profesionales. Complementa a `builder` cuando el recurso a generar es una CLI y no una API web.

---

## Cuándo usar esta guía

Cuando `builder` detecta que el proyecto es una CLI tool (no hay framework HTTP, el `main` es un entry point CLI, o la HU/TT describe "comando", "script automatizado", "utilidad de terminal").

## Stacks recomendados por lenguaje

| Lenguaje | Framework | Mejor para |
|---|---|---|
| **Python** | Click / Typer | Scripts, DevOps tooling, data pipelines con interfaz CLI |
| **Go** | Cobra + Viper | CLIs de alta performance, distribución como binario único |
| **Node.js/TS** | Commander / Clipanion | CLIs para ecosistema npm, herramientas frontend |
| **Rust** | Clap | CLIs de sistema, máxima performance |
| **C#/.NET** | System.CommandLine | Herramientas internas enterprise, ecosistema .NET |
| **Java** | Picocli | CLIs empresariales, integración con Spring Boot |

## Estructura de proyecto (Python + Typer)

```
mi-cli/
├── pyproject.toml
├── src/
│   └── mi_cli/
│       ├── __init__.py
│       ├── main.py              # Entry point: app = typer.Typer()
│       ├── commands/
│       │   ├── __init__.py
│       │   ├── init_cmd.py      # mi-cli init
│       │   └── deploy_cmd.py    # mi-cli deploy
│       ├── core/
│       │   ├── config.py        # Configuración (pydantic-settings)
│       │   └── logging.py       # Logging estructurado
│       └── utils/
└── tests/
    ├── test_init.py
    └── test_deploy.py
```

## Patrones de diseño para CLIs

### 1. Comandos tipados con Typer

```python
# main.py
import typer

app = typer.Typer(help="Mi CLI Tool - automatización de despliegues")
app.add_typer(init_app, name="init")
app.add_typer(deploy_app, name="deploy")

if __name__ == "__main__":
    app()
```

### 2. Configuración validada (pydantic-settings)

```python
# core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MYCLI_", env_file=".env")

    api_url: str = "https://api.default.com"
    log_level: str = "INFO"
    token: str | None = None  # Secreto, solo por env var o archivo

settings = Settings()
```

### 3. Progreso y salida formateada (Rich)

```python
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

console = Console()

def deploy_all(envs: list[str]):
    with Progress() as progress:
        task = progress.add_task("Desplegando...", total=len(envs))
        results = []
        for env in envs:
            try:
                deploy(env)
                results.append((env, "✅", "OK"))
            except Exception as e:
                results.append((env, "❌", str(e)))
            progress.advance(task)

    table = Table(title="Resultado del despliegue")
    table.add_column("Entorno")
    table.add_column("Estado")
    table.add_column("Detalle")
    for r in results:
        table.add_row(*r)
    console.print(table)
```

### 4. Testing de CLI

```python
# tests/test_init.py
from typer.testing import CliRunner
from mi_cli.main import app

runner = CliRunner()

def test_init_creates_config():
    result = runner.invoke(app, ["init", "--name", "test-project"])
    assert result.exit_code == 0
    assert "Proyecto creado" in result.stdout

def test_init_fails_without_name():
    result = runner.invoke(app, ["init"])
    assert result.exit_code != 0
```

### 5. Distribución (pyproject.toml)

```toml
[project]
name = "mi-cli"
version = "1.0.0"
requires-python = ">=3.12"
dependencies = ["typer>=0.12", "rich>=13", "pydantic-settings>=2"]

[project.scripts]
mi-cli = "mi_cli.main:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Stack recomendado por defecto (greenfield CLI)

| Rol | Tecnología |
|---|---|
| Lenguaje | Python 3.12+ (rápido de prototipar) / Go (si binario único es clave) |
| CLI Framework | Typer (Python) / Cobra (Go) / Commander (Node.js) |
| Output formatting | Rich (Python) / lipgloss (Go) / chalk (Node.js) |
| Config | pydantic-settings (Python) / Viper (Go) / cosmiconfig (Node.js) |
| Testing | pytest + typer CliRunner / Go testing + cobra cmd.Execute |
| Distribución | pipx (Python) / go install (Go) / npm global (Node.js) |
